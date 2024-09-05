import axios from 'axios';

const API_BASE_URL = 'http://your-backend-url/api'; // Replace with your backend URL

export const loginUser = async (userID, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/login`, { userID, password });
    return response.data; // Handle the response as needed
  } catch (error) {
    console.error('Error during login', error);
    throw error;
  }
};

export const registerUser = async (userID, password, firstName, phoneNo) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/register`, { userID, password, firstName, phoneNo });
    return response.data; // Handle the response as needed
  } catch (error) {
    console.error('Error during registration', error);
    throw error;
  }
};

