import React, { useState, forwardRef, useImperativeHandle } from 'react';

// The Condition component, using forwardRef to allow parent components to access its internal state and methods.
const Condition = forwardRef(({ id }, ref) => {
  // State to manage the list of uploaded forward files.
  const [forwardFiles, setForwardFiles] = useState([]);
  
  // State to manage the list of uploaded reverse files.
  const [reverseFiles, setReverseFiles] = useState([]);
  
  // State to manage any error messages related to file uploads.
  const [error, setError] = useState('');

  // Expose certain values and methods to parent components via the ref.
  useImperativeHandle(ref, () => ({
    forwardFiles,  // Expose the list of forward files.
    reverseFiles,  // Expose the list of reverse files.
  }));

  // Handle the upload of forward files.
  const handleForwardFileUpload = (e) => {
    // Convert the selected files into an array.
    const selectedFiles = Array.from(e.target.files);
    
    // Check that all selected files have a .wig extension.
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig'));

    if (!isValid) {
      setError('All files must be .wig files.');
      return;
    }

    // Update the state with the new list of forward files.
    setForwardFiles(selectedFiles);

    // Check if the number of forward and reverse files matches.
    if (reverseFiles.length !== selectedFiles.length) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  // Handle the upload of reverse files.
  const handleReverseFileUpload = (e) => {
    // Convert the selected files into an array.
    const selectedFiles = Array.from(e.target.files);
    
    // Check that all selected files have a .wig extension.
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig'));

    if (!isValid) {
      setError('All files must be .wig files.');
      return;
    }

    // Update the state with the new list of reverse files.
    setReverseFiles(selectedFiles);

    // Check if the number of reverse and forward files matches.
    if (forwardFiles.length !== selectedFiles.length) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  // Remove a specific forward file from the list.
  const handleRemoveForwardFile = (index) => {
    const newFiles = [...forwardFiles]; // Create a new array based on the current forward files.
    newFiles.splice(index, 1); // Remove the file at the specified index.
    setForwardFiles(newFiles); // Update the state with the new array.

    // Check if the number of forward and reverse files matches.
    if (newFiles.length !== reverseFiles.length) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  // Remove a specific reverse file from the list.
  const handleRemoveReverseFile = (index) => {
    const newFiles = [...reverseFiles]; // Create a new array based on the current reverse files.
    newFiles.splice(index, 1); // Remove the file at the specified index.
    setReverseFiles(newFiles); // Update the state with the new array.

    // Check if the number of reverse and forward files matches.
    if (newFiles.length !== forwardFiles.length) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  return (
    <div className="condition">
      {/* Display the condition's ID */}
      <h3>Condition {id}</h3>

      {/* Forward Files Upload Section */}
      <div className="form-group">
        <label>Upload forward files:</label>
        <div>
          {/* File input for forward files */}
          <input
            type="file"
            multiple
            onChange={handleForwardFileUpload}
            accept=".wig"
            style={{ display: 'none' }}
            id={`forwardFiles-${id}`} // Unique ID for the input element
          />
          {/* Custom label to trigger the file input */}
          <label htmlFor={`forwardFiles-${id}`} className="custom-file-upload">
            {forwardFiles.length > 0 ? `${forwardFiles.length} Dateien ausgewählt` : 'Dateien auswählen'}
          </label>
        </div>
        {/* Display a list of uploaded forward files with a remove button for each */}
        {forwardFiles.map((file, index) => (
          <div className="overviewOfFiles" key={index}>
            <p>{file.name}</p>
            <button className='remove-button' onClick={() => handleRemoveForwardFile(index)}>Remove</button>
          </div>
        ))}
      </div>

      {/* Reverse Files Upload Section */}
      <div className="form-group">
        <label>Upload reverse files:</label>
        <div>
          {/* File input for reverse files */}
          <input
            type="file"
            multiple
            onChange={handleReverseFileUpload}
            accept=".wig"
            style={{ display: 'none' }}
            id={`reverseFiles-${id}`} // Unique ID for the input element
          />
          {/* Custom label to trigger the file input */}
          <label htmlFor={`reverseFiles-${id}`} className="custom-file-upload">
            {reverseFiles.length > 0 ? `${reverseFiles.length} Dateien ausgewählt` : 'Dateien auswählen'}
          </label>
        </div>
        {/* Display a list of uploaded reverse files with a remove button for each */}
        {reverseFiles.map((file, index) => (
          <div className="overviewOfFiles" key={index}>
            <p>{file.name}</p>
            <button className='remove-button' onClick={() => handleRemoveReverseFile(index)}>Remove</button>
          </div>
        ))}
      </div>

      {/* Display an error message if there is one */}
      {error && <p className="error">{error}</p>}
    </div>
  );
});

export default Condition;
