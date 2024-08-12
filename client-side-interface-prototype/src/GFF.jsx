import React, { useState, forwardRef, useImperativeHandle } from 'react';

// The GFF component, using forwardRef to allow parent components to access its internal state and methods.
const GFF = forwardRef((props, ref) => {
  // State to manage the uploaded GFF file.
  const [file, setFile] = useState(null);

  // Expose the `file` state to parent components via the ref.
  useImperativeHandle(ref, () => ({
    file, // Expose the uploaded GFF file.
  }));

  // Handle the GFF file upload.
  const handleFileUpload = (e) => {
    const selectedFile = e.target.files[0]; // Get the selected file from the input event.
    setFile(selectedFile); // Update the state with the selected file.
  };

  // Handle the removal of the uploaded GFF file.
  const handleRemoveFile = () => {
    setFile(null); // Clear the file state, effectively removing the file.
  };

  return (
    <div className="form-group">
      {/* Label for the GFF file upload section */}
      <label><b>Upload GFF-file:</b></label>
      
      {/* File input for uploading the GFF file */}
      <input
        type="file"
        onChange={handleFileUpload}
        accept=".gff" // Restrict the input to only accept .gff files.
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

export default GFF;
