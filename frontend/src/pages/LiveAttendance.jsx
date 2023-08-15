import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './LiveAttendance.css';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
function LiveAttendance() {
  const [videoStream, setVideoStream] = useState(null);

  useEffect(() => {
    startVideoStream();
    return () => {
      if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const startVideoStream = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      setVideoStream(stream);

      const videoElement = document.getElementById('video');
      videoElement.srcObject = stream;
    } catch (error) {
      console.error('Error starting video stream:', error);
    }
  };

  const captureFrame = async () => {
    try {
      const videoElement = document.getElementById('video');
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      canvas.getContext('2d').drawImage(videoElement, 0, 0, canvas.width, canvas.height);

      const imageData = canvas.toDataURL('image/jpeg');
      console.log(imageData);

      await axios.post('http://127.0.0.1:8000/api/mark-attendance/', { image: imageData }).then(result=>{
        console.log(result);
        Swal.fire({
          icon: 'success',
          title: 'Marked!',
          text: 'Your Attendance Marked successfully!',
        })
      });

      console.log('Attendance marked successfully');
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Sorry!',
        text: 'Could not Find You!',
      })
      console.error('Error marking attendance:', error);
    }
  };


  const handleCheckOut = async () => {
    try {
      const videoElement = document.getElementById('video');
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      canvas.getContext('2d').drawImage(videoElement, 0, 0, canvas.width, canvas.height);

      const imageData = canvas.toDataURL('image/jpeg');
      console.log(imageData);

      await axios.post('http://127.0.0.1:8000/api/attendance-checkout/', { image: imageData }).then(result=>{
        console.log(result);
        Swal.fire({
          icon: 'success',
          title: 'Marked!',
          text: 'Your Checkout Marked successfully!',
        })
      });

      console.log('Attendance marked successfully');
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Sorry!',
        text: 'Could not Find You!',
      })
      console.error('Error marking attendance:', error);
    }
  };

  const navigate = useNavigate();
  const handleRegisterUser = () => {
    navigate('/register'); // Navigate to the user registration page
  };

  return (
    <div className="live-attendance">
      <h2>Live Attendance</h2>
      <video id="video" autoPlay></video>
      <div className="button-group">
        <button className="check-button" onClick={captureFrame}>Check In</button>
        <button className="check-button" onClick={handleCheckOut}>Check Out</button>
        <button className="register-button" onClick={handleRegisterUser}>Register User</button> {/* Add this button */}
      </div>
    </div>
  );
}

export default LiveAttendance;
