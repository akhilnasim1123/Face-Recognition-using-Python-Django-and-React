import React from 'react';
import { BrowserRouter as Router,Route,Routes } from 'react-router-dom';
import LiveAttendance from './pages/LiveAttendance';
import UserRegistration from './pages/UserRegistration';
import Login from './pages/admin/login';
import AdminPage from './pages/admin/AdminPage';

function App() {
  return (
    <Router>
   <Routes>

    <Route element={<LiveAttendance/>} path= '/'/>
    <Route element={<UserRegistration/>} path= '/register'/>
    <Route element={<Login/>} path= '/admin'/>
    <Route element={<AdminPage/>} path= '/admin-home'/>


    </Routes>
    </Router>
  );
}

export default App;
