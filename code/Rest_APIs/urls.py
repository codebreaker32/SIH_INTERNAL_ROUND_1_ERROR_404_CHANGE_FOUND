from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    UserProfileView, 
    UserChangePasswordView, 
    GetDiabetesDataView, 
    PatientDataView, 
    DoctorPatientListView, 
    UserLogoutView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('get-diabetes-data/', GetDiabetesDataView.as_view(), name='get-diabetes-data'),
    path('doctor/patients/', DoctorPatientListView.as_view(), name='doctor_patient_list'),
    path('patients/', PatientDataView.as_view(), name='patient_list_create'),
    path('patients/<str:username>/', PatientDataView.as_view(), name='patient_detail_update_delete'),
]
