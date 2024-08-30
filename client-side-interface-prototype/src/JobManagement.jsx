import React, { useState, useEffect } from 'react';
import './App.css';
import './JobManagement.css';
import { useNavigate } from 'react-router-dom';

function JobManagement() {

  // State to store the list of projects fetched from the server.
  const [projects, setProjects] = useState([]);
  /* 
  Example projects data structure:
  projects = [["project1", "Project Alpha"], ["project2", "Project Beta"]] 
  */

  // State to store the conditions for each project.
  const [projectConditions, setProjectConditions] = useState({});
  /* 
  Example projectConditions data structure:
   projectConditions = {
     project1: [["Condition A", "condition1"],["Condition B", "condition2"]],
     project2: [["Condition X", "condition3"],["Condition Y", "condition4"]]}
  */
 
  // State to store the job IDs for each condition.
  const [conditionsJobs, setConditionsJobs] = useState({});
  /* 
  Example Job IDs data structure:
  conditionsJobs = {condition1: { forward: "job1_forward", reverse: "job1_reverse" },
                    condition2: { forward: "job2_forward", reverse: "job2_reverse" }}
  */

  // State to store the status of each job.
  const [jobStatuses, setJobStatuses] = useState({});
  /* 
  Example jobStatuses data structure:
   jobStatuses = {
    job1_forward: "Finished",
    job1_reverse: "Running",
    job2_forward: "Not started",
    job2_reverse: "Finished",
  }
  */

  // Use the useNavigate hook to navigate to a different page.
  const navigate = useNavigate();

  // State to manage the project ID that is currently being downloaded.
  const [loadingProjectId, setLoadingProjectId] = useState(null);

  // State to manage the feedback message displayed while downloading.
  const [feedbackMessage, setFeedbackMessage] = useState('');

  // Fetch data from the server when the page loads.
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch all projects that are currently in the database
        const projectResponse = await fetch('/api/get_project_list');
        // Check if the response is ok and throw an error if it is not
        if (!projectResponse.ok) {
          throw new Error('Failed to fetch project list.');
        }
        const projectData = await projectResponse.json();
        // Set the projects state to the project data
        setProjects(Object.entries(projectData));

        // Fetch conditions for each project
        const conditions = {};
        // Loop through each project and fetch the conditions for each project
        for (const [projectId] of Object.entries(projectData)) {
          const conditionsResponse = await fetch(`/api/get_conditions?project_id=${projectId}`);
          if (!conditionsResponse.ok) {
            throw new Error(`Failed to fetch conditions for project ${projectId}.`);
          }
          // Set the conditions state to the conditions data
          const conditionsData = await conditionsResponse.json();
          conditions[projectId] = Object.entries(conditionsData);
        }
        setProjectConditions(conditions);

        // Fetch job IDs and statuses for each condition
        const jobs = {};
        const statuses = {};
        // Loop through each project and fetch the job IDs and statuses for each condition
        for (const projectId in conditions) {
          for (const [, conditionId] of conditions[projectId]) {
            const jobIdsResponse = await fetch(`/api/get_jobids?condition_id=${conditionId}`);
            if (!jobIdsResponse.ok) {
              throw new Error(`Failed to fetch job IDs for condition ${conditionId}.`);
            }
            // Set the jobs state to the job IDs data
            const jobIdsData = await jobIdsResponse.json();
            jobs[conditionId] = jobIdsData;

            // Fetch the status of each job
            const forwardStatusResponse = await fetch(`/api/get_state?jobid=${jobIdsData.forward}`);
            const reverseStatusResponse = await fetch(`/api/get_state?jobid=${jobIdsData.reverse}`);
            if (forwardStatusResponse.ok && reverseStatusResponse.ok) {
              const forwardStatus = await forwardStatusResponse.json();
              const reverseStatus = await reverseStatusResponse.json();
              statuses[jobIdsData.forward] = forwardStatus["Job status"];
              statuses[jobIdsData.reverse] = reverseStatus["Job status"];
            } else {
              throw new Error(`Failed to fetch job statuses for condition ${conditionId}.`);
            }
          }
        }
        // Set the jobStatuses state to the statuses data
        setConditionsJobs(jobs);
        setJobStatuses(statuses);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  // Function to render the status of a job
  const renderStatus = (status) => {
    // Return different colors based on the status of the job
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

  // Function to check if a condition is finished
  const isConditionFinished = (conditionId) => {
    const jobIds = conditionsJobs[conditionId];
    return jobIds && jobStatuses[jobIds.forward] === 'Finished' && jobStatuses[jobIds.reverse] === 'Finished';
  }

  // Function to check if a project is finished
  const isProjectFinished = (projectId) => {
    const conditions = projectConditions[projectId];
    return conditions && conditions.every(([, conditionId]) => isConditionFinished(conditionId));
  };

  // Function to handle viewing a condition
  const handleViewCondition = (conditionId) => {
    // Navigate to the visualization page for the selected condition
    navigate(`/visualization/${conditionId}`);
  };

  // function for refreshing the jobmanagement page
  function refreshPage() {
    window.location.reload();
  }

  // Function to handle downloading project data
  const handleDownloadProject = async (projectId) => {
    try {
        // Set loading state and feedback message
        setLoadingProjectId(projectId);
        setFeedbackMessage('Downloading project data, please wait...');

        const response = await fetch(`/api/get_zip_file?project_id=${projectId}`);
        if (!response.ok) {
            throw new Error('Failed to download project.');
        }
        // Convert the response to a blob and create a URL for downloading
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        // Set the download attribute to the project ID
        a.download = `${projectId}.zip`;
        // Append the anchor element to the body and click it to start the download
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

 // Component for rendering individual job status
 const JobStatus = ({ jobId, status }) => (
   <div>
    Job ID: {jobId}, Status: {renderStatus(status)}
    </div>
  );

 // Component for rendering individual conditions
 const Condition = ({ conditionName, conditionId }) => (
  <div className="condition-box">
    <h3>{conditionName}</h3>
      <div>
        <JobStatus jobId={conditionsJobs[conditionId]?.forward} status={jobStatuses[conditionsJobs[conditionId]?.forward]} />
        <JobStatus jobId={conditionsJobs[conditionId]?.reverse} status={jobStatuses[conditionsJobs[conditionId]?.reverse]} />
      </div>
      <button
        className={`view-condition-button ${isConditionFinished(conditionId) ? 'finished' : 'unfinished'}`}
        onClick={() => handleViewCondition(conditionId)}
        disabled={!isConditionFinished(conditionId)}
      >
        View Condition
      </button>
    </div>
  );

  // Component for rendering individual projects
  const Project = ({ projectId, projectName }) => (
    <div className="project-box">
      <h2>{projectName}</h2>
      <button
        className={`download-button ${isProjectFinished(projectId) ? 'finished' : 'unfinished'}`}
        onClick={() => handleDownloadProject(projectId)}
        disabled={!isProjectFinished(projectId) || loadingProjectId === projectId}
      >
        {loadingProjectId === projectId ? 'Downloading...' : 'Download Project Data'}
      </button>
      <div>
        {projectConditions[projectId]?.map(([conditionName, conditionId]) => (
          <Condition key={conditionId} conditionName={conditionName} conditionId={conditionId} />
        ))}
      </div>
    </div>
  );

  // Render the JobManagement component
  return (
    <div className="App">
      <div className="projects-container">
        <h1>Project Manager</h1>
        <button className="refresh-button" onClick={() => window.location.reload()}>Refresh Statuses</button>
        {feedbackMessage && <p className="feedback-message-download">{feedbackMessage}</p>}
        <div>
          {projects.map(([projectId, projectName]) => (
            <Project key={projectId} projectId={projectId} projectName={projectName} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default JobManagement;
