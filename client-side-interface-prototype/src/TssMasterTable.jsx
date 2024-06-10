import React, { useState, forwardRef, useImperativeHandle } from 'react';

// The TssMasterTable component, using forwardRef to allow parent components to access its internal state and methods.
const TssMasterTable = forwardRef((props, ref) => {
  // State to manage the uploaded master table file.
  const [file, setFile] = useState(null);

  // Expose the `file` state to parent components via the ref.
  useImperativeHandle(ref, () => ({
    file, // Expose the uploaded master table file.
  }));

  // Handle the master table file upload.
  const handleFileUpload = (e) => {
    const selectedFile = e.target.files[0]; // Get the selected file from the input event.
    setFile(selectedFile); // Update the state with the selected file.
  };

  // Handle the removal of the uploaded master table file.
  const handleRemoveFile = () => {
    setFile(null); // Clear the file state, effectively removing the file.
  };

  return (
    <div className="form-group">
      {/* Label for the master table file upload section */}
      <label><b>Upload master table from TSS predator (optional):</b></label>
      
      {/* File input for uploading the master table file */}
      <input
        type="file"
        onChange={handleFileUpload}
        accept=".tsv" // Restrict the input to only accept .tsv files.
        style={{ display: file ? 'none' : 'block' }} // Hide the input if a file is already uploaded.
      />
      
      {/* Display the uploaded file details if a file is selected */}
      {file && (
        <div className="file-details">
          <p>{file.name}</p> {/* Display the name of the uploaded file */}
          <button className="remove-button" onClick={handleRemoveFile}>Remove</button> {/* Button to remove the file */}
        </div>
      )}
    </div>
  );
});

export default TssMasterTable;
