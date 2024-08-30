import React from 'react';

function FileList({ files, onRemove }) {
  return (
    <div>
      {files.map((file, index) => (
        <div className="overviewOfFiles" key={index}>
          <p>{file.name}</p>
          <button className='remove-button' onClick={() => onRemove(index)}>Remove</button>
        </div>
      ))}
    </div>
  );
}

export default FileList;
