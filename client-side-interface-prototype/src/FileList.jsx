import React from 'react';

// The FileList component is responsible for displaying a list of uploaded files with the option to remove them.
function FileList({ files, onRemove }) {
  return (
    <div>
      {/* Iterate over the files array and display each file with a remove button */}
      {files.map((file, index) => (
        <div className="overviewOfFiles" key={index}>
          {/* Display the file name */}
          <p>{file.name}</p>
          {/* Button to remove the file, calls the onRemove function with the file's index */}
          <button className='remove-button' onClick={() => onRemove(index)}>Remove</button>
        </div>
      ))}
    </div>
  );
}

export default FileList;
