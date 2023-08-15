import React, { useState } from 'react';
import UserManagement from './UserManagement';
import AttendanceReport from './AttendanceReport';
import './admin.css';

function AdminPage() {
  const [activeTab, setActiveTab] = useState('userManagement');

  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="admin-page">
      <div className="sidebar">
        <button
          className={`sidebar-button ${activeTab === 'userManagement' ? 'active' : ''}`}
          onClick={() => handleTabClick('userManagement')}
        >
          User Management
        </button>
        <button
          className={`sidebar-button ${activeTab === 'attendanceReport' ? 'active' : ''}`}
          onClick={() => handleTabClick('attendanceReport')}
        >
          Attendance Report
        </button>
      </div>
      <div className="content">
        {activeTab === 'userManagement' && <UserManagement />}
        {activeTab === 'attendanceReport' && <AttendanceReport />}
      </div>
    </div>
  );
}

export default AdminPage;
