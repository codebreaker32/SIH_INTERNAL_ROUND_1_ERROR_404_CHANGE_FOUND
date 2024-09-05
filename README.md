# AI-ENHANCED HEALTHCARE DIAGNOSTICS AND MANAGEMENT SYSTEM INSPIRED BY ZK MEDICAL BILLING PLATFORM

This README provides an overview of the project, including team details, relevant links, tasks completed, tech stack, key features, and steps to run the project locally.

## Team Details

**Team Name:** ERROR 404 : CHANGE FOUND?

**Project Title** - HEALTHCARE MANAGEMENT AND RECOMMENDER SYSTEM 

**Team Leader:** [@HARSHDIPSAHA](https://github.com/HARSHDIPSAHA)

**Team Members:**

- **ANSHUMAN RAJ** - 2023UCD3053 - [@SAVAGECAT05](https://github.com/SAVAGECAT05)
- **HEMANK KAUSHIK** - 2023UEI2867 - [@HEMANKKAUSHIK](https://github.com/HEMANKKAUSHIK)
- **KANISHK SHARMA** - 2023UCD2175 - [@GHOSTDOG007](https://github.com/GHOSTDOG007)
- **ANSHIKA SINGH** - 2023UCA1946 - [@CUBIX33](https://github.com/CUBIX33)
- **HARSHDIP SAHA** - 2023UCA1897 - [@HARSHDIPSAHA](https://github.com/HARSHDIPSAHA)
- **AMAN BIHARI** - 2023UCA1910 - [@CODEBREAKER32](https://github.com/CODEBREAKER32)

**PROJECT DESCRIPTION** - This system addresses the inefficiencies in current healthcare diagnostics and management by implementing AI models that can analyze patient data for more accurate and timely diagnosis, offer predictive insights for preventive care. This automation reduces human error, improves decision-making, and enhances patient care.The project is running fine on local host and the frontend part is deployed.

**TECHNOLOGIES USED** :- <br>
*1. DJANGO* <br>
*2. REACT JS* <br>
*3. SQLite* <br>
*4. PANDAS* <br>
*5. GEMINI* <br>
*6. MATPLOTLIB* <br>
*7. OPENCV* <br>
*8. TESSERACT OCR* <br>
*9. XAI (SHAP)* <br>
*10. XGboost* <br>
## Project Links

- **Internal Presentation:** [Internal Presentation](https://github.com/codebreaker32/SIH_INTERNAL_ROUND_1_ERROR_404_CHANGE_FOUND/blob/main/files/Internal_PPT_ERROR404_CHANGE_FOUND.pdf)
- **Final SIH Presentation:** [Final SIH Presentation](https://github.com/codebreaker32/SIH_INTERNAL_ROUND_1_ERROR_404_CHANGE_FOUND/blob/main/files/SIH_PPT_ERROR404_CHANGE_FOUND.pdf)
- **Video Demonstration:** [Watch Video](https://youtu.be/XL4BwAEqjc4)
- **Live Deployment:** [View Deployment](https://healthy002.netlify.app/)
- **Source Code:** [GitHub Repository](https://github.com/codebreaker32/SIH_INTERNAL_ROUND_1_ERROR_404_CHANGE_FOUND)

# Django Backend 

This project is a Django-based backend for managing diabetes patient data, providing user authentication, patient data handling, and integration with machine learning models for outcome predictions and recommendations.

## Features
- User registration and login with JWT-based authentication.
- Role-based access control for patients and doctors.
- CRUD operations for diabetes data.
- Machine learning-based outcome prediction and health recommendations.
- Patient details extraction from uploaded images (for doctors).
- Secure password management and user profile functionality.
- RESTful APIs using Django Rest Framework (DRF).
- CORS support.

## Technologies Used
- **Django**: Backend web framework.
- **Django REST Framework (DRF)**: To create and handle REST APIs.
- **JWT (SimpleJWT)**: For token-based user authentication.
- **Google Generative AI**: Integrated for additional recommendation generation.
- **OpenCV** and **Tesseract**: For image processing and extracting patient details from images.
- **XGBoost**: For diabetes prediction models.
- **Pandas**, **NumPy**, and **Scikit-Learn**: For data manipulation and ML logic.
  
## Prerequisites

- Python 3.8+
- A virtual environment is recommended for project dependencies.

## Setup Instructions

### 1. Clone the repository
git clone <https://github.com/codebreaker32/SIH_INTERNAL_ROUND_1_ERROR_404_CHANGE_FOUND.git>
cd <HealthCare_BACKEND>

### 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  
For Windows, use `venv\Scripts\activate`

### 3. Install the dependencies
pip install -r requirements.txt

### 4. Setup the Django project (migrate database and create superuser)
python manage.py migrate
python manage.py createsuperuser

### 5. Run the server
python manage.py runserver
