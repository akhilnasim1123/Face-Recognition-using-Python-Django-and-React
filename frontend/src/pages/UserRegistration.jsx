import React, { useState, useRef } from 'react';
import axios from 'axios';
import './UserRegistration.css';
import {useNavigate} from 'react-router-dom'
import Swal from 'sweetalert2';

function UserRegistration() {
  const [name, setName] = useState('');
  const [imageData, setImageData] = useState(null);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const handleNameChange = (event) => {
    setName(event.target.value);
  };
  const navigate = useNavigate()
  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error('Error starting webcam:', error);
    }
  };

  const stopWebcam = () => {
    if (videoRef.current) {
      videoRef.current.srcObject?.getTracks().forEach(track => track.stop());
    }
  };

  const captureFrame = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

      const capturedImageData = canvas.toDataURL('image/jpeg');
      console.log(capturedImageData);
      setImageData(capturedImageData);
    }
  };

  const handleRegister = async () => {
    if (name && imageData) {
      try {
        await axios.post('http://127.0.0.1:8000/register/registration-requests/', { name, image: imageData }).then(
          Swal.fire({
            icon: 'success',
            title: 'User Registered!',
            text: 'User registered successfully!',
          })

        ).then(
          navigate('/')
        )

      } catch (error) {
        console.error('Error registering user:', error);
        
        // Display SweetAlert error message
        Swal.fire({
          icon: 'error',
          title: 'Registration Error',
          text: 'Error registering user. Please try again.',
        });
      }
    } else {
      // Display SweetAlert warning message
      Swal.fire({
        icon: 'warning',
        title: 'Incomplete Information',
        text: 'Please provide a name and select an image.',
      });
    }
  };

  return (
    <div className="user-registration">
      <h2>User Registration</h2>
      <div className="webcam-container">
        <video ref={videoRef} autoPlay></video>
        <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
        <div className="webcam-buttons">
          <button onClick={startWebcam}>Start Webcam</button>
          <button onClick={captureFrame}>Capture Image</button>
          <button onClick={stopWebcam}>Stop Webcam</button>
        </div>
      </div>
      <div className="registration-form">
        <input type="text" placeholder="Enter your name" value={name} onChange={handleNameChange} />
        <button className="register-button" onClick={handleRegister}>Register</button>
      </div>
    </div>
  );
}

export default UserRegistration;
