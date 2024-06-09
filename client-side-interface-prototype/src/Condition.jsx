import React, { useState, forwardRef, useImperativeHandle } from 'react';

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

    if (reverseFiles.length !== selectedFiles.length) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  const handleReverseFileUpload = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const isValid = selectedFiles.every(file => file.name.endsWith('.wig'));

    if (!isValid) {
      setError('All files must be .wig files.');
      return;
    }

    setReverseFiles(selectedFiles);

    if (forwardFiles.length !== selectedFiles.length) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  const handleRemoveForwardFile = (index) => {
    const newFiles = [...forwardFiles];
    newFiles.splice(index, 1);
    setForwardFiles(newFiles);

    if (newFiles.length !== reverseFiles.length) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  const handleRemoveReverseFile = (index) => {
    const newFiles = [...reverseFiles];
    newFiles.splice(index, 1);
    setReverseFiles(newFiles);

    if (newFiles.length !== forwardFiles.length) {
      setError('The number of forward and reverse files must match.');
    } else {
      setError('');
    }
  };

  return (
    <div className="condition">
      <h3>Condition {id}</h3>
      <div className="form-group">
        <label>Upload forward files:</label>
        <div>
          <input
            type="file"
            multiple
            onChange={handleForwardFileUpload}
            accept=".wig"
            style={{ display: 'none' }}
            id={`forwardFiles-${id}`}
          />
          <label htmlFor={`forwardFiles-${id}`} className="custom-file-upload">
            {forwardFiles.length > 0 ? `${forwardFiles.length} Dateien ausgewählt` : 'Dateien auswählen'}
          </label>
        </div>
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
          <input
            type="file"
            multiple
            onChange={handleReverseFileUpload}
            accept=".wig"
            style={{ display: 'none' }}
            id={`reverseFiles-${id}`}
          />
          <label htmlFor={`reverseFiles-${id}`} className="custom-file-upload">
            {reverseFiles.length > 0 ? `${reverseFiles.length} Dateien ausgewählt` : 'Dateien auswählen'}
          </label>
        </div>
        {reverseFiles.map((file, index) => (
          <div className="overviewOfFiles" key={index}>
            <p>{file.name}</p>
            <button className='remove-button' onClick={() => handleRemoveReverseFile(index)}>Remove</button>
          </div>
        ))}
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
});

export default Condition;
