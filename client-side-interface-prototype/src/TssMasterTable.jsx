import React, { useState, forwardRef, useImperativeHandle } from 'react';

const TssMasterTable = forwardRef((props, ref) => {
  const [file, setFile] = useState(null);

  useImperativeHandle(ref, () => ({
    file,
  }));

  const handleFileUpload = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleRemoveFile = () => {
    setFile(null);
  };

  return (
    <div className="form-group">
      <label><b>Upload master table from TSS predator (optional):</b></label>
      <input
        type="file"
        onChange={handleFileUpload}
        accept=".tsv"
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
});

export default TssMasterTable;
