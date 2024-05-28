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
    setFiles(selectedFiles);
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
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Condition;
