## Tasks Accomplished

- [x] **Patient Management Dashboard:**
- [x] **Personalized Treatment Recommendations:** 
- [x] **AI-Powered Diagnostics:**

## Technology Stack

This project leverages the following technologies:

**[Tesseract OCR](https://github.com/tesseract-ocr/tesseract):** Efficiently extracts text from scanned medical documents, enabling digitization of physical health records.

**[XGBoost](https://xgboost.readthedocs.io/):** Provides accurate predictions on diabetes status, known for its speed and performance in machine learning tasks.

**[SQLite](https://www.sqlite.org/index.html):** Lightweight, file-based database for easy data management, ideal for small to medium-scale applications.

**[Django](https://www.djangoproject.com/):** Manages backend logic, security, and database interactions, ensuring robust and scalable web applications.

**[React.js](https://reactjs.org/):** Builds dynamic and responsive user interfaces, enhancing the user experience with interactive components.

**[Gemini Pro](https://deepmind.google/technologies/gemini/pro/):** Offers personalized AI-driven health recommendations, tailoring healthcare insights to individual needs.


## Key Features

- **Real-Time Data Integration:** Seamlessly updates patient information from multiple sources in real-time for accurate monitoring.
- **Advanced AI Analytics:** Utilizes AI to predict health risks and offer personalized treatment recommendations.
- **User-Friendly Interface:** Provides an intuitive dashboard for easy navigation and access to essential healthcare tools.
- **Automated Test Result Processing:** Uses Tesseract OCR to automatically extract and digitize information from uploaded medical documents.
- **Secure Data Management:** Utilizes SQLite for storing patient and doctor data securely, with Django handling backend operations and data privacy. We do not share any patient data (ID or name) directly with Gemini Pro.
- **Fine-Tuned Chatbot:** A NLP chatbot on diabetes data and knowledge that provides personalized support.When user logins, he/she will be able to see a chatbot with which they can interact for diet/exercises in the context of diabetes.



## Local Setup Instructions (Write for both windows and macos)

Follow these steps to run the project locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/codebreaker32/SIH_INTERNAL_ROUND_1_ERROR_404_CHANGE_FOUND
   cd REPO_DIRECTORY
   ```
2. **Set up Tesseract ocr**
   ```bash
   follow documentation: https://github.com/tesseract-ocr/tesseract
   ```


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

# REACT FRONTEND 
This project is a React-based frontend for managing diabetes patient data, integrating with a Django backend to provide user interfaces for patient data management, user authentication, and integration with machine learning models.

## Features
- User-friendly interface for patient and doctor interactions.
- Role-based access control views for patients and doctors.
- Forms for CRUD operations related to diabetes data.
- Integration with backend APIs for data handling and predictions.
- Image upload functionality for extracting patient details (doctor-specific).
- Responsive design for a seamless user experience.

## Technologies Used
- React: Frontend library for building the user interface.
- React Router: For routing and navigation within the application.
- Axios: For making HTTP requests to the backend APIs.
- Material-UI or Bootstrap: For UI components and styling.
- Redux: For state management. 
- React Hook Form: For form handling.

## Prerequisites
- Node.js (v14.x or later)
- npm (v6.x or later) or yarn.

## Setup instructions 

### 1. Clone the repository 
git clone <https://github.com/codebreaker32/SIH_INTERNAL_ROUND_1_ERROR_404_CHANGE_FOUND.git>
cd <code>

### 2. Install the dependencies 
npm install
npm install react-scripts 
npm install react-router-dom

### 3. Start the development server
npm start

### 4. 4. Build for production (optional)
npm run build





 

