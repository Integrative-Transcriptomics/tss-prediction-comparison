// JobManagement.jsx
import React from 'react';
import { useLocation } from 'react-router-dom';

function JobManagement() {
  // to access the projectName we access the passed state from the first page with useLocation
  const location = useLocation();
  // if the projectName is undefined for whatever reason the default projectName is empty
  const { projectName } = location.state || { projectName: 'Default Project Name' };

  // To test whether or not the backend sends a .json we fetch the response from the backend endpoint that 
  // sends the .json. In our case the endpoint is '/upload'.
  // statevariable for storing the jsondata we (hopefully) receive
  const [jsonData, setJsonData] = useState({});
  // we can control the way data is fetched by using useEffect and its dependency array
  useEffect(() => {
    // method for fetching a json object asynchronically
    const fetchJsonData = async () => {
      try {
        // json comes from the backend endpoint '/upload'
        const response = await fetch('/upload');
        // check if we successfully requested 
        if (!response.ok) {
          throw new Error('Network does not respond.');
        }
        // set the state to the data we receive out of our request
        const data = await response.json();
        setJsonData(data); 
      } catch (error) {
        console.error('Could not fetch: ', error);
      }
    };
    // fetch the data 
    fetchJsonData();
    // here we only want to fetch once so we set the array to empty
  }, []); 

  return (
    <div>
      <h1>Job Management</h1>
      <p>Project Name: {projectName}</p>
      <div>{jsonData ? JSON.stringify(jsonData) : 'Data cannot be printed'}</div>
    </div>
  );
}

export default JobManagement;