// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProjectForm from './ProjectForm';
import JobManagement from './JobManagement';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<ProjectForm />} />
          <Route path="/job-management" element={<JobManagement />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
