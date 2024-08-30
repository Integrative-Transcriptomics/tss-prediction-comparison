import React from 'react';

// The FileUpload component handles the display and selection of files for uploading.
function FileUpload({ label, onChange, files, id }) {
  return (
    <div className="form-group">
      {/* Label for the file input field */}
      <label>{label}</label>
      <div>
        {/* Hidden file input element, styled to not be visible */}
        <input
          type="file"
          multiple
          onChange={onChange}
          accept=".wig"
          style={{ display: 'none' }}
          id={id}
        />
        {/* Custom label acting as a button to trigger the file input */}
        <label htmlFor={id} className="custom-file-upload">
          {/* Display the number of selected files or prompt to select files */}
          {files.length > 0 ? `${files.length} files selected` : 'Select files'}
        </label>
      </div>
    </div>
  );
}

export default FileUpload;
