import React, { useState, forwardRef, useImperativeHandle } from 'react';
import FileUpload from './FileUpload';
import FileList from './FileList';

const Condition = forwardRef(({ id }, ref) => {
  const [forwardFiles, setForwardFiles] = useState([]);
  const [reverseFiles, setReverseFiles] = useState([]);
  const [error, setError] = useState('');

  useImperativeHandle(ref, () => ({
    forwardFiles,
    reverseFiles,
  }));

  const handleForwardFileUpload = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig'));

    if (!isValid) {
      setError('All files must be .wig files.');
      return;
    }

    setForwardFiles(selectedFiles);
    validateFileCounts(selectedFiles.length, reverseFiles.length);
  };

  const handleReverseFileUpload = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig'));

    if (!isValid) {
      setError('All files must be .wig files.');
      return;
    }

    setReverseFiles(selectedFiles);
    validateFileCounts(forwardFiles.length, selectedFiles.length);
  };

  const handleRemoveForwardFile = (index) => {
    const newFiles = [...forwardFiles];
    newFiles.splice(index, 1);
    setForwardFiles(newFiles);
    validateFileCounts(newFiles.length, reverseFiles.length);
  };

  const handleRemoveReverseFile = (index) => {
    const newFiles = [...reverseFiles];
    newFiles.splice(index, 1);
    setReverseFiles(newFiles);
    validateFileCounts(forwardFiles.length, newFiles.length);
  };

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

      <FileUpload
        label="Upload forward files:"
        onChange={handleForwardFileUpload}
        files={forwardFiles}
        id={`forwardFiles-${id}`}
      />
      <FileList files={forwardFiles} onRemove={handleRemoveForwardFile} />

      <FileUpload
        label="Upload reverse files:"
        onChange={handleReverseFileUpload}
        files={reverseFiles}
        id={`reverseFiles-${id}`}
      />
      <FileList files={reverseFiles} onRemove={handleRemoveReverseFile} />

      {/* Fehler wird nur einmal hier gerendert */}
      {error && <p className="error">{error}</p>}
    </div>
  );
});

export default Condition;
