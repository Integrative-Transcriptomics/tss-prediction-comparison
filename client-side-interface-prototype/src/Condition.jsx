import React, { useState } from 'react';

function Condition({ id }) {
  // State variables to store forward and reverse files and any error messages
  const [forwardFiles, setForwardFiles] = useState([]);
  const [reverseFiles, setReverseFiles] = useState([]);
  const [error, setError] = useState('');

  // Handler function for uploading forward files
  const handleForwardFileUpload = (e) => {
    const selectedFiles = Array.from(e.target.files); // Convert file list to array
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig')); // Check if all files are .wig files

    if (!isValid) {
      setError('All files must be .wig files.'); // Set error if any file is not .wig
      return;
    }

    setForwardFiles(selectedFiles); // Update state with selected forward files

    if (reverseFiles.length !== selectedFiles.length) {
      setError('The number of forward and reverse files must match.'); // Set error if the number of files do not match
    } else {
      setError(''); // Clear error if the number of files match
    }
  };

  // Handler function for uploading reverse files
  const handleReverseFileUpload = (e) => {
    const selectedFiles = Array.from(e.target.files); // Convert file list to array
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig')); // Check if all files are .wig files

    if (!isValid) {
      setError('All files must be .wig files.'); // Set error if any file is not .wig
      return;
    }

    setReverseFiles(selectedFiles); // Update state with selected reverse files

    if (forwardFiles.length !== selectedFiles.length) {
      setError('The number of forward and reverse files must match.'); // Set error if the number of files do not match
    } else {
      setError(''); // Clear error if the number of files match
    }
  };

  // Handler function for removing a forward file
  const handleRemoveForwardFile = (index) => {
    const newFiles = [...forwardFiles]; // Create a copy of the forward files array
    newFiles.splice(index, 1); // Remove the file at the specified index
    setForwardFiles(newFiles); // Update state with the new array

    if (newFiles.length !== reverseFiles.length) {
      setError('The number of forward and reverse files must match.'); // Set error if the number of files do not match
    } else {
      setError(''); // Clear error if the number of files match
    }
  };

  // Handler function for removing a reverse file
  const handleRemoveReverseFile = (index) => {
    const newFiles = [...reverseFiles]; // Create a copy of the reverse files array
    newFiles.splice(index, 1); // Remove the file at the specified index
    setReverseFiles(newFiles); // Update state with the new array

    if (newFiles.length !== forwardFiles.length) {
      setError('The number of forward and reverse files must match.'); // Set error if the number of files do not match
    } else {
      setError(''); // Clear error if the number of files match
    }
  };

  return (
    <div className="condition">
      <h3>Condition {id}</h3>
      <div className="form-group">
        <label>Upload forward files:</label>
        <div>
          {/* Hidden file input for forward files */}
          <input
            type="file"
            multiple
            onChange={handleForwardFileUpload}
            accept=".wig"
            style={{ display: 'none' }}
            id={`forwardFiles-${id}`}
          />
          {/* Custom label that looks like a button */}
          <label htmlFor={`forwardFiles-${id}`} className="custom-file-upload">
            {forwardFiles.length > 0 ? `${forwardFiles.length} Dateien ausgewählt` : 'Dateien auswählen'}
          </label>
        </div>
        {/* List of uploaded forward files with remove buttons */}
        {forwardFiles.map((file, index) => (
          <div className="overviewOfFiles" key={index}>
            <p>{file.name}</p>
            <button className='remove-button' onClick={() => handleRemoveForwardFile(index)}>Remove</button>
          </div>
        ))}
      </div>
      <div className="form-group">
        <label>Upload reverse files:</label>
        <div>
          {/* Hidden file input for reverse files */}
          <input
            type="file"
            multiple
            onChange={handleReverseFileUpload}
            accept=".wig"
            style={{ display: 'none' }}
            id={`reverseFiles-${id}`}
          />
          {/* Custom label that looks like a button */}
          <label htmlFor={`reverseFiles-${id}`} className="custom-file-upload">
            {reverseFiles.length > 0 ? `${reverseFiles.length} Dateien ausgewählt` : 'Dateien auswählen'}
          </label>
        </div>
        {/* List of uploaded reverse files with remove buttons */}
        {reverseFiles.map((file, index) => (
          <div className="overviewOfFiles" key={index}>
            <p>{file.name}</p>
            <button className='remove-button' onClick={() => handleRemoveReverseFile(index)}>Remove</button>
          </div>
        ))}
      </div>
      {/* Display error message if any */}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Condition;
