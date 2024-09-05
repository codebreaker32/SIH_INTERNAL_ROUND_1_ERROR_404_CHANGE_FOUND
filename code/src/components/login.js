import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Import the CSS file
import axios from 'axios';

const LoginPage = ({ role }) => {
  const navigate = useNavigate();
  const [userID, setUserID] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [phoneNo, setPhoneNo] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isSignup, setIsSignup] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('/api/login/', {
        username: userID,
        password: password,
      });
      localStorage.setItem('access_token', response.data.token.access);
      localStorage.setItem('refresh_token', response.data.token.refresh);
      if (role === 'doctor') {
        navigate('/doctor-dashboard');
      } else {
        navigate('/patient-dashboard');
      }
    } catch (error) {
      setError('Username or Password is not Valid');
    }
  };

  const handleSignUp = async () => {
    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      return;
    }
    if (firstName && phoneNo && password && confirmPassword) {
      try {
        // Make a POST request to register a new user
        const response = await axios.post('/api/register/', {
          username: userID,
          password: password,
          first_name: firstName,
          phone_no: phoneNo,
        });
        alert('Sign-up successful! You can now log in.');
        setIsSignup(false);
      } catch (error) {
        setError('Error occurred during sign-up.');
      }
    } else {
      alert('Please fill out all fields.');
    }
  };

  return (
    <div className="login-container">
      <h1 className="login-title">
        {isSignup ? 'Patient ' : (role === 'doctor' ? 'Doctor' : 'Patient')} {isSignup ? 'Sign Up' : 'Login'}
      </h1>
      {error && <p className="error-message">{error}</p>}
      {isSignup ? (
        <div className="login-form">
          <input
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className="login-input"
          />
          <input
            type="text"
            placeholder="Phone No"
            value={phoneNo}
            onChange={(e) => setPhoneNo(e.target.value)}
            className="login-input"
          />
          <input
            type="text"
            placeholder="User ID"
            value={userID}
            onChange={(e) => setUserID(e.target.value)}
            className="login-input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-input"
          />
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="login-input"
          />
          <button onClick={handleSignUp} className="login-button">Sign Up</button>
          <p>Already have an account? <button onClick={() => setIsSignup(false)} className="toggle-button">Login</button></p>
        </div>
      ) : (
        <div className="login-form">
          <input
            type="text"
            placeholder="Enter User ID"
            value={userID}
            onChange={(e) => setUserID(e.target.value)}
            className="login-input"
          />
          <input
            type="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-input"
          />
          <button onClick={handleLogin} className="login-button">Login</button>
          {role === 'patient' && (
            <div className="signup-option">
              <p>Don't have an account?</p>
              <button onClick={() => setIsSignup(true)} className="signup-button">
                Sign Up
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LoginPage;

