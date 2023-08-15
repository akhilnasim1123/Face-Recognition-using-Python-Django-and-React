import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './UserManagement.css';

function UserManagement() {
  const [students, setStudents] = useState([]);
  const [registrationRequests, setRegistrationRequests] = useState([]);

  useEffect(() => {
    fetchStudents();
    fetchRegistrationRequests();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/admin-side/students/');
      setStudents(response.data.students || []); // Set to an empty array if undefined
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  };

  const fetchRegistrationRequests = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/admin-side/registration-requests/');
      setRegistrationRequests(response.data.registrationRequests || []); // Set to an empty array if undefined
    } catch (error) {
      console.error('Error fetching registration requests:', error);
    }
  };

  const handleApproveRequest = async (requestId) => {
    try {
      await axios.post(`http://127.0.0.1:8000/admin-side/approve-request/${requestId}/`);
      fetchRegistrationRequests();
    } catch (error) {
      console.error('Error approving request:', error);
    }
  };

  const handleIgnoreRequest = async (requestId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/admin/registration-requests/${requestId}/`);
      fetchRegistrationRequests();
    } catch (error) {
      console.error('Error ignoring request:', error);
    }
  };

  console.log('students:', students);
  console.log('registrationRequests:', registrationRequests);

  return (
    <div className="user-management">
      <h2>User Management</h2>
      
      {students.length > 0 && (
        <div className="students">
          <h3>Students</h3>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                {/* Add more columns as needed */}
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student.id}>
                  <td>{student.id}</td>
                  <td>{student.name}</td>
                  {/* Add more cells based on the columns */}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {registrationRequests.length > 0 && (
        <div className="registration-requests">
          <h3>Registration Requests</h3>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {registrationRequests.map((request) => (
                <tr key={request.id}>
                  <td>{request.id}</td>
                  <td>{request.name}</td>
                  <td>
                    <button onClick={() => handleApproveRequest(request.id)}>Approve</button>
                    <button onClick={() => handleIgnoreRequest(request.id)}>Ignore</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default UserManagement;
