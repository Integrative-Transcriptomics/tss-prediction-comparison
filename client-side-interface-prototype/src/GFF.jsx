import React, { useState } from 'react';

function GFF() {
  const [file, setFile] = useState(null);

  const handleFileUpload = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleRemoveFile = () => {
    setFile(null);
  };

  return (
    <div className="form-group">
      <label><b>Upload GFF-file (optional):</b></label>
      <input
        type="file"
        onChange={handleFileUpload}
        accept=".gff"
        style={{ display: file ? 'none' : 'block' }}
      />
      {file && (
        <div className="file-details">
          <p>{file.name}</p>
          <button className="remove-button" onClick={handleRemoveFile}>Remove</button>
        </div>
      )}
    </div>
  );
}

export default GFF;
