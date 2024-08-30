import React, { useState, forwardRef, useImperativeHandle } from 'react';
import FileUpload from './FileUpload';
import FileList from './FileList';

// The Condition component uses forwardRef to pass a ref object from a parent component.
// This allows the parent component to access internal states (forwardFiles and reverseFiles) of this component.
const Condition = forwardRef(({ id }, ref) => {
  // useState hooks to store the uploaded files and handle error messages.
  const [forwardFiles, setForwardFiles] = useState([]);
  const [reverseFiles, setReverseFiles] = useState([]);
  const [error, setError] = useState('');

  // The useImperativeHandle hook makes the files (forwardFiles and reverseFiles) accessible to parent components.
  useImperativeHandle(ref, () => ({
    forwardFiles,
    reverseFiles,
  }));

  // Handler for uploading forward files. Here, the files are validated to ensure they have the .wig extension.
  const handleForwardFileUpload = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig'));

    // If any file does not have the .wig extension, set an error message.
    if (!isValid) {
      setError('All files must be .wig files.');
      return;
    }

    // If all files are valid, update the state with the new files.
    setForwardFiles(selectedFiles);
    // Check if the number of forward and reverse files match.
    validateFileCounts(selectedFiles.length, reverseFiles.length);
  };

  // Similar handler for uploading reverse files.
  const handleReverseFileUpload = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig'));

    // If any file does not have the .wig extension, set an error message.
    if (!isValid) {
      setError('All files must be .wig files.');
      return;
    }

    // If all files are valid, update the state with the new files.
    setReverseFiles(selectedFiles);
    // Check if the number of forward and reverse files match.
    validateFileCounts(forwardFiles.length, selectedFiles.length);
  };

  // Handler for removing a forward file from the list.
  const handleRemoveForwardFile = (index) => {
    const newFiles = [...forwardFiles];
    // Remove the file at the specified index.
    newFiles.splice(index, 1);
    setForwardFiles(newFiles);
    // Revalidate the file counts after removal.
    validateFileCounts(newFiles.length, reverseFiles.length);
  };

  // Handler for removing a reverse file from the list.
  const handleRemoveReverseFile = (index) => {
    const newFiles = [...reverseFiles];
    // Remove the file at the specified index.
    newFiles.splice(index, 1);
    setReverseFiles(newFiles);
    // Revalidate the file counts after removal.
    validateFileCounts(forwardFiles.length, newFiles.length);
  };

  // Function to validate that the number of forward and reverse files are equal.
  const validateFileCounts = (forwardCount, reverseCount) => {
    if (forwardCount !== reverseCount) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  return (
    <div className="condition">
      <h3>Condition {id}</h3>

      {/* File upload for forward files */}
      <FileUpload
        label="Upload forward files:"
        onChange={handleForwardFileUpload}
        files={forwardFiles}
        id={`forwardFiles-${id}`}
      />
      {/* Display the list of uploaded forward files */}
      <FileList files={forwardFiles} onRemove={handleRemoveForwardFile} />

      {/* File upload for reverse files */}
      <FileUpload
        label="Upload reverse files:"
        onChange={handleReverseFileUpload}
        files={reverseFiles}
        id={`reverseFiles-${id}`}
      />
      {/* Display the list of uploaded reverse files */}
      <FileList files={reverseFiles} onRemove={handleRemoveReverseFile} />

      {/* Display error message if there's any */}
      {error && <p className="error">{error}</p>}
    </div>
  );
});

export default Condition;
