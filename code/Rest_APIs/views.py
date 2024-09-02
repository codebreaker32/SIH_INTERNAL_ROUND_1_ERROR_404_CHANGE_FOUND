from .models import MyUser
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
import pickle
import os
from .utils import ml_generate_outcome
from .utils2 import generate_recommendation

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'Rest_APIs', 'diabetes_xgb.pkl')
with open(file_path, 'rb') as file:
    model = pickle.load(file)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            return Response({'errors': {'non_field_errors': ['Username or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    def post(self, request, format=None):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(serializer.validated_data['refresh_token'])
            token.blacklist()
            return Response({'msg': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'errors': {'non_field_errors': ['Invalid token or token has already been blacklisted.']}}, status=status.HTTP_400_BAD_REQUEST)

class GetDiabetesDataView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        diabetes_data = DiabetesData.objects.filter(user=user)
        serializer = DiabetesDataSerializer(diabetes_data, many=True)

        if diabetes_data.exists():
            latest_data = diabetes_data.latest('date_time')
            validated_data = {
                'pregnancies': latest_data.pregnancies,
                'glucose': latest_data.glucose,
                'blood_pressure': latest_data.blood_pressure,
                'skin_thickness': latest_data.skin_thickness,
                'insulin': latest_data.insulin,
                'bmi': latest_data.bmi,
                'diabetes_pedigree_function': latest_data.diabetes_pedigree_function,
                'age': latest_data.age,
            }
            recommendation, outcome, anomaly_status, proba_diabetic = generate_recommendation(validated_data)
        else:
            recommendation = "No data available."
            anomaly_status = ""
            proba_diabetic = None

        response_data = {
            'diabetes_data': serializer.data,
            'recommendation': recommendation,
            'anomaly_status': anomaly_status,
            'proba_diabetic': proba_diabetic
        }
        return Response(response_data)

class DoctorPatientListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.role != 'doctor':
            raise PermissionDenied("You do not have permission to perform this action.")
        patients = MyUser.objects.filter(role='patient').prefetch_related('diabetes_records')
        serializer = PatientWithDiabetesDataSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientDataView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None, format=None):
        if username:
            try:
                patient = MyUser.objects.get(username=username, role='patient')
                diabetes_data = DiabetesData.objects.filter(user=patient)
                if diabetes_data.exists():
                    for data in diabetes_data:
                        if data.outcome is None:
                            data.outcome = ml_generate_outcome(data)
                            data.save()
                    serializer = DiabetesDataSerializer(diabetes_data, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"detail": "No diabetes data found for this patient."}, status=status.HTTP_404_NOT_FOUND)
            except MyUser.DoesNotExist:
                raise NotFound("Patient not found.")
        else:
            if request.user.role != 'doctor':
                raise PermissionDenied("You do not have permission to perform this action.")
            
            patients = MyUser.objects.filter(role='patient')
            result = []
            for patient in patients:
                diabetes_data = DiabetesData.objects.filter(user=patient)
                if diabetes_data.exists():
                    for data in diabetes_data:
                        if data.outcome is None:
                            data.outcome = ml_generate_outcome(data)
                            data.save()
                    serializer = DiabetesDataSerializer(diabetes_data, many=True)
                    result.append({
                        'id': patient.pk,
                        'username': patient.username,
                        'diabetes_data': serializer.data
                    })
            return Response(result, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.role != 'doctor':
            raise PermissionDenied("You do not have permission to perform this action.")

        if 'image' in request.data:
            serializer = PatientDetailsExtractionSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                extracted_data = serializer.save()
                return Response(extracted_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserWithDiabetesDataSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = serializer.save()
                diabetes_data_records = DiabetesData.objects.filter(user=user)
                for diabetes_data in diabetes_data_records:
                    if diabetes_data.outcome is None:
                        diabetes_data.outcome = ml_generate_outcome(diabetes_data)
                        diabetes_data.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username, format=None):
        if request.user.role != 'doctor':
            raise PermissionDenied("You do not have permission to perform this action.")

        try:
            patient = MyUser.objects.get(username=username, role='patient')
            diabetes_data = DiabetesData.objects.get(user=patient)
        except (MyUser.DoesNotExist, DiabetesData.DoesNotExist):
            raise NotFound("Diabetes data or patient not found.")
        
        serializer = UserWithDiabetesDataSerializer(patient, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            diabetes_data_records = DiabetesData.objects.filter(user=user)
            for diabetes_data in diabetes_data_records:
                diabetes_data.outcome = ml_generate_outcome(diabetes_data)
                diabetes_data.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        if request.user.role != 'doctor':
            raise PermissionDenied("You do not have permission to perform this action.")

        try:
            patient = MyUser.objects.get(username=username, role='patient')
            diabetes_data = DiabetesData.objects.filter(user=patient)
        except MyUser.DoesNotExist:
            raise NotFound("Patient not found.")
        
        if not diabetes_data.exists():
            return Response({"detail": "No diabetes data found for this patient."}, status=status.HTTP_404_NOT_FOUND)

        diabetes_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
