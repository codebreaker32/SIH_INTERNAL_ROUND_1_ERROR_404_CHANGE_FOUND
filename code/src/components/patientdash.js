import React, { useState, useEffect } from 'react';
import axios from 'axios'; // If using axios
import './patientdash.css';

// Add chart components if using Chart.js
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register necessary chart components
Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const PatientDashboard = () => {
  const [patientName, setPatientName] = useState('');
  const [patientID, setPatientID] = useState('');
  const [age, setAge] = useState('');
  const [view, setView] = useState('details'); // State to manage view
  const [analyticsData, setAnalyticsData] = useState(null);
  const [recommendations, setRecommendations] = useState(null);

  const handleViewChange = (viewType) => {
    setView(viewType);
    if (viewType === 'analytics') {
      fetchAnalyticsData();
    } else if (viewType === 'recommendations') {
      fetchRecommendations();
    }
  };

  const fetchPatientDetails = async () => {
    try {
      const response = await axios.get(`/api/patient/${patientID}`); // Replace with actual endpoint
      setPatientName(response.data.name);
      setAge(response.data.age);
    } catch (error) {
      console.error('Error fetching patient details:', error);
    }
  };

  const fetchAnalyticsData = async () => {
    try {
      const response = await axios.get(`/api/analytics/${patientID}`); // Replace with actual endpoint
      setAnalyticsData(response.data);
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(`/api/recommendations/${patientID}`); // Replace with actual endpoint
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  useEffect(() => {
    if (patientID) {
      fetchPatientDetails();
    }
  }, [patientID]);

  return (
    <div className="patient-dashboard-container">
      <h1 className="dashboard-title">Patient Dashboard</h1>

      {/* Patient Details Section */}
      {view === 'details' && (
        <div className="patient-details">
          <h2 className="details-title">Patient Details</h2>
          <p><strong>Name:</strong> {patientName || 'Loading...'}</p>
          <p><strong>ID:</strong> {patientID}</p>
          <p><strong>Age:</strong> {age || 'Loading...'}</p>
          <div className="view-options">
            <button onClick={() => handleViewChange('analytics')} className={`view-button ${view === 'analytics' ? 'active' : ''}`}>View Analytics</button>
            <button onClick={() => handleViewChange('recommendations')} className={`view-button ${view === 'recommendations' ? 'active' : ''}`}>Check Recommendations</button>
          </div>
        </div>
      )}

      {/* Analytics Section */}
      {view === 'analytics' && analyticsData && (
        <div className="analytics-section">
          <h2 className="section-title">Patient Analytics</h2>
          <Line
            data={analyticsData}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                tooltip: {
                  callbacks: {
                    label: function (context) {
                      return `${context.dataset.label}: ${context.raw}`;
                    },
                  },
                },
              },
            }}
          />
          <button onClick={() => handleViewChange('details')} className="back-button">Back to Details</button>
        </div>
      )}

      {/* Recommendations Section */}
      {view === 'recommendations' && recommendations && (
        <div className="recommendations-section">
          <h2 className="section-title">Recommendations</h2>
          <div className="recommendations-content">
            {/* Display recommendations */}
            <h3 className="subsection-title">Diet</h3>
            <ul>
              {recommendations.diet.map((item, index) => (
                <li key={index}><strong>{item.title}:</strong> {item.description}</li>
              ))}
            </ul>

            {/* Exercises Section */}
            <h3 className="subsection-title">Exercises</h3>
            <ul>
              {recommendations.exercises.map((exercise, index) => (
                <li key={index}>{exercise}</li>
              ))}
            </ul>

            {/* Routine Section */}
            <h3 className="subsection-title">Routine</h3>
            <ul>
              {recommendations.routine.map((routine, index) => (
                <li key={index}>{routine}</li>
              ))}
            </ul>

            {/* Educational Facts Section */}
            <h3 className="subsection-title">Educational Facts in a Funny Way</h3>
            <ul>
              {recommendations.educationalFacts.map((fact, index) => (
                <li key={index}><strong>{fact.question}</strong> {fact.answer}</li>
              ))}
            </ul>

            {/* Anomaly Status Section */}
            <h3 className="subsection-title">Anomaly Status</h3>
            <p><em>{recommendations.anomalyStatus}</em></p>
          </div>
          <button onClick={() => handleViewChange('details')} className="back-button">Back to Details</button>
        </div>
      )}
    </div>
  );
};

export default PatientDashboard;

