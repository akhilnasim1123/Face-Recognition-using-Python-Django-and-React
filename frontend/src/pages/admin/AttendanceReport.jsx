import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AttendanceReport.css';

function AttendanceReport() {
  const [attendanceData, setAttendanceData] = useState([]);

  useEffect(() => {
    fetchAttendanceData();
  }, []);

  const fetchAttendanceData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/admin-side/attendance-report/');
      setAttendanceData(response.data.attendanceReport || []); // Set to an empty array if undefined
    } catch (error) {
      console.error('Error fetching attendance report:', error);
    }
  };

  const isLateCheckIn = (checkInTime) => {
    const checkIn = new Date(checkInTime);
    return checkIn.getHours() > 9 || (checkIn.getHours() === 9 && checkIn.getMinutes() > 0);
  };

  return (
    <div className="attendance-report">
      <h2>Attendance Report</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Student ID</th>
            <th>Student Name</th>
            <th>Check-in Time</th>
            <th>Check-out Time</th>
          </tr>
        </thead>
        <tbody>
          {attendanceData.map((attendance) => (
            <tr key={attendance.id} className={isLateCheckIn(attendance.check_in_time) ? 'late-check-in' : ''}>
              <td>{attendance.date}</td>
              <td>{attendance.student_id}</td>
              <td>{attendance.student_name}</td>
              <td>{attendance.check_in_time}</td>
              <td>{attendance.check_out_time || 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AttendanceReport;
