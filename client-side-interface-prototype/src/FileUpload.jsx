import React from 'react';

function FileUpload({ label, onChange, files, id }) {
  return (
    <div className="form-group">
      <label>{label}</label>
      <div>
        <input
          type="file"
          multiple
          onChange={onChange}
          accept=".wig"
          style={{ display: 'none' }}
          id={id}
        />
        <label htmlFor={id} className="custom-file-upload">
          {files.length > 0 ? `${files.length} Dateien ausgewählt` : 'Dateien auswählen'}
        </label>
      </div>
    </div>
  );
}

export default FileUpload;
