import React, { useState } from 'react';

function Condition({ id }) {
  const [replicates, setReplicates] = useState('');
  const [files, setFiles] = useState([]);
  const [error, setError] = useState('');
  

  const handleReplicatesChange = (e) => {
    setReplicates(e.target.value);
    setFiles([]); // Reset the files when the number of replicates changes
  };

  const handleFileUpload = (e) => {
    //
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > replicates) {
      setError(`You can only upload ${replicates} files.`);
      return;
    }

    const isValid = selectedFiles.every(file => file.name.endsWith('.wig'));
    if (!isValid) {
      setError('All files must be .wig files.');
      return;
    }

    setError('');
    /*whenever more than 1 file is uploaded we overwrote the current state. With this line instead of 
      overwriting the state we append the newly selected file to the previously selected files. 
      Syntax:
      prevFiles is a parameter fo the arrow function. Its the previous state and inside the square brackets 
      is the new state. The dots are the spread operator, put them in front of an array and you get all elements of 
      the array. 
    */
    setFiles(prevFiles => [...prevFiles, ...selectedFiles]);
  };

  return (
    <div className="condition">
      <h3>Condition {id}</h3>
      <div className="form-group">
        <label>Replicates:</label>
        <input
          type="number"
          value={replicates}
          onChange={handleReplicatesChange}
          placeholder="Number of Replicates"
        />
      </div>
      <div className="form-group">
        <label>Upload Replicates:</label>
        <input
          type="file"
          multiple
          onChange={handleFileUpload}
          accept=".wig"
          disabled={!replicates}
        />
        {files.map((file, index) => (
          <p key={index}>
            {file.name}
          </p>
        ))}
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Condition;
