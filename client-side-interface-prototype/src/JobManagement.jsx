import React, { useState, useEffect } from 'react';
import './App.css';
import './JobManagement.css';
import { useNavigate } from 'react-router-dom';

function JobManagement() {

  // State to store the list of projects fetched from the server.
  const [projects, setProjects] = useState([]);
  // State to store the conditions for each project.
  const [projectConditions, setProjectConditions] = useState({});
  // State to store the job IDs for each condition.
  const [conditionsJobs, setConditionsJobs] = useState({});
  // State to store the status of each job.
  const [jobStatuses, setJobStatuses] = useState({});
  // Use the useNavigate hook to navigate to a different page.
  const navigate = useNavigate();
  // State to manage loading state and feedback message for project download
  const [loadingProjectId, setLoadingProjectId] = useState(null);
  const [feedbackMessage, setFeedbackMessage] = useState('');

  useEffect(() => {
    // Fetch all projects that are currently in the database
    const fetchProjects = async () => {
      try {
        const response = await fetch('/api/get_project_list');
        if (!response.ok) {
          // If the response is not successful, throw an error
          throw new Error('Failed to fetch project list.');
        }
        // Parse the response data as JSON
        const data = await response.json();
        // Update the state with the fetched projects
        setProjects(Object.entries(data));
      } catch (error) {
        console.error('Error fetching project list:', error);
      }
    };

    fetchProjects();
  }, []);

  useEffect(() => {
    // Fetch conditions for each project
    const fetchConditions = async () => {
      try {
        // Fetch conditions for each project
        const conditions = {};
        for (const [projectId] of projects) {
          const response = await fetch(`/api/get_conditions?project_id=${projectId}`);
          if (!response.ok) {
            throw new Error(`Failed to fetch conditions for project ${projectId}.`);
          }
          // Parse the response data as JSON
          const data = await response.json();
          // Store the conditions for each project
          conditions[projectId] = Object.entries(data);
        }
        // Update the state with the fetched conditions
        setProjectConditions(conditions);
      } catch (error) {
        console.error('Error fetching conditions:', error);
      }
    };

    if (projects.length > 0) {
      // Fetch conditions for each project if projects exist
      fetchConditions();
    }
  }, [projects]);

  useEffect(() => {
    // Fetch job IDs and statuses for each condition
    const fetchJobs = async () => {
      try {
        const jobs = {};
        const statuses = {};
        // Fetch job IDs for each condition
        for (const projectId in projectConditions) {
          // Iterate over the conditions for each project
          for (const [, conditionId] of projectConditions[projectId]) {
            const response = await fetch(`/api/get_jobids?condition_id=${conditionId}`);
            if (!response.ok) {
              throw new Error(`Failed to fetch job IDs for condition ${conditionId}.`);
            }
            const data = await response.json();
            jobs[conditionId] = data;

            // Fetch job statuses
            const forwardStatusResponse = await fetch(`/api/get_state?jobid=${data.forward}`);
            const reverseStatusResponse = await fetch(`/api/get_state?jobid=${data.reverse}`);
            // Check if the responses are successful
            if (forwardStatusResponse.ok && reverseStatusResponse.ok) {
              // Parse the response data as JSON
              const forwardStatus = await forwardStatusResponse.json();
              const reverseStatus = await reverseStatusResponse.json();
              // Store the job statuses
              statuses[data.forward] = forwardStatus["Job status"];
              statuses[data.reverse] = reverseStatus["Job status"];
            } else {
              throw new Error(`Failed to fetch job statuses for condition ${conditionId}.`);
            }
          }
        }
        setConditionsJobs(jobs);
        setJobStatuses(statuses);
      } catch (error) {
        console.error('Error fetching job IDs and statuses:', error);
      }
    };

    // Fetch job IDs and statuses for each condition if conditions exist
    if (Object.keys(projectConditions).length > 0) {
      fetchJobs();
    }
  }, [projectConditions]);

  // Function to render the status of a job
  const renderStatus = (status) => {
    switch (status) {
      case 'Not started':
        return <span style={{ color: 'gray' }}>Not started</span>;
      case 'Running':
        return <span style={{ color: 'blue' }}>Running</span>;
      case 'Finished':
        return <span style={{ color: 'green' }}>Finished</span>;
      case 'Failed':
        return <span style={{ color: 'red' }}>Failed</span>;
      default:
        return <span>Unknown status</span>;
    }
  };

  const isConditionFinished = (conditionId) => {
    const jobIds = conditionsJobs[conditionId];
    return jobIds && jobStatuses[jobIds.forward] === 'Finished' && jobStatuses[jobIds.reverse] === 'Finished';
  }

  const isProjectFinished = (projectId) => {
    const conditions = projectConditions[projectId];
    return conditions && conditions.every(([, conditionId]) => isConditionFinished(conditionId));
  };

  const handleViewCondition = (conditionId) => {
    // Navigate to the visualization page for the selected condition
    navigate(`/visualization/${conditionId}`);
  };

  // function for refreshing the jobmanagement page
  function refreshPage() {
    window.location.reload();
  }

  const handleDownloadProject = async (projectId) => {
    try {
        // Set loading state and feedback message
        setLoadingProjectId(projectId);
        setFeedbackMessage('Downloading project data, please wait...');

        const response = await fetch(`/api/get_zip_file?project_id=${projectId}`);
        if (!response.ok) {
            throw new Error('Failed to download project.');
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${projectId}.zip`;
        document.body.appendChild(a);
        a.click();
        a.remove();

        // Update feedback message on success
        setFeedbackMessage('Project data downloaded successfully.');
    } catch (error) {
        console.error('Error downloading project:', error);
        setFeedbackMessage('Failed to download project data.');
    } finally {
        // Reset loading state
        setLoadingProjectId(null);
    }
};

  // Render the list of projects, conditions, and job statuses
  return (
      <div className="App">
        <div className="projects-container">
            <h1>Project Manager</h1>
            <button className="refresh-button" onClick={refreshPage}>Refresh Statuses</button>
            {feedbackMessage && <p className="feedback-message-donwload">{feedbackMessage}</p>} {/* Display feedback message */}
            <ul>
                {projects.map(([projectId, projectName]) => (
                    <div key={projectId} className="project-box">
                        <h2>{projectName}</h2>
                        <button 
                            className={`download-button ${isProjectFinished(projectId) ? 'finished' : 'unfinished'}`} 
                            onClick={() => handleDownloadProject(projectId)} 
                            disabled={!isProjectFinished(projectId) || loadingProjectId === projectId}
                        >
                            {loadingProjectId === projectId ? 'Downloading...' : 'Download Project Data'}
                        </button>
                        <ul>
                            {projectConditions[projectId]?.map(([conditionName, conditionId], index) => (
                                <li key={conditionId} className="condition-box">
                                    <h3>{conditionName}</h3>
                                    <ul>
                                        <li>
                                            Forward Job ID: {conditionsJobs[conditionId]?.forward}, Status: {renderStatus(jobStatuses[conditionsJobs[conditionId]?.forward])}
                                        </li>
                                        <li>
                                            Reverse Job ID: {conditionsJobs[conditionId]?.reverse}, Status: {renderStatus(jobStatuses[conditionsJobs[conditionId]?.reverse])}
                                        </li>
                                    </ul>
                                    <button 
                                        className={`view-condition-button ${isConditionFinished(conditionId) ? 'finished' : 'unfinished'}`}
                                        onClick={() => handleViewCondition(conditionId)}
                                        disabled={!isConditionFinished(conditionId)}
                                    >
                                        View Condition
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </ul>
        </div>
  </div>
  );
}

export default JobManagement;
