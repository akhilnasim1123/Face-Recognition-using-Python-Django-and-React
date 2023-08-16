import React, { useState } from 'react';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import 'primeflex/primeflex.css';
import axios from 'axios';
import './admin.css';
import Swal from 'sweetalert2';
import { useNavigate } from 'react-router-dom';
function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/admin-side/login/', {
        username,
        password,
      });
      console.log(response);
      // const data = await response.json();
      // console.log(data);
      if (response.status === 200){
        Swal.fire({
            icon: 'success',
            title: 'Welcome!',
            text: 'Logged In successfully!',
          }).then(result=>{
            navigate('/admin-home')
          })
      }

      // Handle successful login, e.g., redirect to a dashboard
    } catch (error) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h2>Login</h2>
        <span className="p-float-label">
          <InputText
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <label htmlFor="username">Username</label>
        </span>
        <span className="p-float-label">
          <InputText
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <label htmlFor="password">Password</label>
        </span>
        <Button label="Login" onClick={handleLogin} className="p-button-raised p-button-rounded" />
        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

export default Login;
