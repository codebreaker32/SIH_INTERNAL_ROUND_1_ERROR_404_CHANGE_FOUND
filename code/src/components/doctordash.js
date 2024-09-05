import React, { useState } from 'react';
import axios from 'axios'; // Import axios for making HTTP requests
import './doctordash.css';

const DoctorDashboard = () => {
  const [patientID, setPatientID] = useState('');
  const [patientName, setPatientName] = useState('');
  const [uploadType, setUploadType] = useState('');
  const [prescriptionFile, setPrescriptionFile] = useState(null);
  const [prescriptionDetails, setPrescriptionDetails] = useState({
    pregnancies: '',
    glucose: '',
    bloodPressure: '',
    skinThickness: '',
    insulin: '',
    bmi: '',
    diabetesPedigreeFunction: '',
    age: '',
  });
  const [patientFound, setPatientFound] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('access_token')); // Retrieve token from local storage

  const handleFileUpload = (e) => {
    setPrescriptionFile(e.target.files[0]);
  };

  const handleManualDetailChange = (e) => {
    const { name, value } = e.target;
    setPrescriptionDetails((prevDetails) => ({
      ...prevDetails,
      [name]: value
    }));
  };

  const handlePatientSearch = async () => {
    try {
      const response = await axios.get(`/api/patients/${patientID}/`, {
        headers: {
          Authorization: `Bearer ${token}` // Include token in the request header
        }
      });
      setPatientName(response.data.username); // Adjust according to your actual response structure
      setPatientFound(true);
    } catch (error) {
      alert('Patient not found. Please check the Patient ID.');
      setPatientFound(false);
      setPatientName('');
    }
  };

  const handleSubmit = async () => {
    if (uploadType === 'file' && prescriptionFile) {
      const formData = new FormData();
      formData.append('image', prescriptionFile);
      try {
        await axios.post(`/api/patients/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${token}` // Include token in the request header
          }
        });
        alert(`Test Results for ${patientName} uploaded successfully.`);
      } catch (error) {
        alert('Failed to upload test results.');
      }
    } else if (uploadType === 'manual' && Object.values(prescriptionDetails).every(detail => detail)) {
      try {
        await axios.post(`/api/patients/`, prescriptionDetails, {
          headers: {
            Authorization: `Bearer ${token}` // Include token in the request header
          }
        });
        alert(`Test results for ${patientName} entered successfully.`);
      } catch (error) {
        alert('Failed to enter test results.');
      }
    } else {
      alert('Please complete the form.');
    }

    // Clear the form fields
    setPatientID('');
    setPatientName('');
    setUploadType('');
    setPrescriptionFile(null);
    setPrescriptionDetails({
      pregnancies: '',
      glucose: '',
      bloodPressure: '',
      skinThickness: '',
      insulin: '',
      bmi: '',
      diabetesPedigreeFunction: '',
      age: '',
    });
    setPatientFound(false);
  };

  return (
    <div className="doctor-dashboard-container">
      <h1 className="doctor-dashboard-title">Doctor Dashboard</h1>
      <div className="doctor-form">
        <input
          type="text"
          placeholder="Patient ID"
          value={patientID}
          onChange={(e) => setPatientID(e.target.value)}
          className="form-input"
        />
        <button onClick={handlePatientSearch} className="form-button">Search</button>

        {patientFound && (
          <>
            <p>Patient Name: {patientName}</p>
            <div className="upload-options">
              <label className="option-label">
                <input
                  type="radio"
                  value="file"
                  checked={uploadType === 'file'}
                  onChange={() => setUploadType('file')}
                />
                Upload Test Results (Image/PDF)
              </label>
              <label className="option-label">
                <input
                  type="radio"
                  value="manual"
                  checked={uploadType === 'manual'}
                  onChange={() => setUploadType('manual')}
                />
                Enter Test Result Details Manually
              </label>
            </div>

            {uploadType === 'file' && (
              <div className="file-upload">
                <input
                  type="file"
                  accept="image/*,application/pdf"
                  onChange={handleFileUpload}
                  className="file-input"
                />
              </div>
            )}

            {uploadType === 'manual' && (
              <div className="manual-form">
                <input
                  type="text"
                  name="pregnancies"
                  placeholder="Pregnancies"
                  value={prescriptionDetails.pregnancies}
                  onChange={handleManualDetailChange}
                  className="form-input"
                />
                <input
                  type="number"
                  name="glucose"
                  placeholder="Glucose"
                  value={prescriptionDetails.glucose}
                  onChange={handleManualDetailChange}
                  className="form-input"
                />
                <input
                  type="number"
                  name="bloodPressure"
                  placeholder="Blood Pressure"
                  value={prescriptionDetails.bloodPressure}
                  onChange={handleManualDetailChange}
                  className="form-input"
                />
                <input
                  type="number"
                  name="skinThickness"
                  placeholder="Skin Thickness"
                  value={prescriptionDetails.skinThickness}
                  onChange={handleManualDetailChange}
                  className="form-input"
                />
                <input
                  type="number"
                  name="insulin"
                  placeholder="Insulin"
                  value={prescriptionDetails.insulin}
                  onChange={handleManualDetailChange}
                  className="form-input"
                />
                <input
                  type="number"
                  name="bmi"
                  placeholder="BMI"
                  value={prescriptionDetails.bmi}
                  onChange={handleManualDetailChange}
                  className="form-input"
                />
                <input
                  type="number"
                  name="diabetesPedigreeFunction"
                  placeholder="Diabetes Pedigree Function"
                  value={prescriptionDetails.diabetesPedigreeFunction}
                  onChange={handleManualDetailChange}
                  className="form-input"
                />
                <input
                  type="number"
                  name="age"
                  placeholder="Age"
                  value={prescriptionDetails.age}
                  onChange={handleManualDetailChange}
                  className="form-input"
                />
              </div>
            )}

            <button onClick={handleSubmit} className="form-button">
              Submit
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default DoctorDashboard;

