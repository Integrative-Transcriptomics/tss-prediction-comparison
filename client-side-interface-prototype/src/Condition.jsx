import React, { useState } from 'react';

function Condition({ id }) {
  const [replicates, setReplicates] = useState('');
  const [files, setFiles] = useState([]);
  const [error, setError] = useState('');
  

  const handleReplicatesChange = (e) => {
    setReplicates(e.target.value);
    setFiles([]); // Reset the files when the number of replicates changes
  };

  // to remove the file at the given index from the array without directly changing the current state
  // we remove the file from a copy of files of the current state and return the updated copy
  // splice(index, 1) removes 1 element at the index index
  const handleRemoveFile = (index) => {
    const newFiles = [...files];
    newFiles.splice(index, 1); 
    setFiles(newFiles);
  }
  const handleFileUpload = (e) => {
    // if the user double-clicks a file in his explorer selectedFiles only contains that file
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
    /*whenever more than 1 file is uploaded we overwrote the current state. With this line instead of 
      overwriting the state we append the newly selected file to the previously selected files. 
      Syntax:
      prevFiles is a parameter fo the arrow function. Its the previous state and inside the square brackets 
      is the new state. The dots are the spread operator, put them in front of an array and you get all elements of 
      the array. 
    */
    setFiles(prevFiles => [...prevFiles, ...selectedFiles]);
  };

  return (
    // the files.map creates a paragraph for each file with the specific index
    // inside the .map we can also add a button so that one button for each file is created, this
    // button needs to call the file-remove-handler 
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

        {files.map((file, index) => (
          <div key={index}>
            <p>
              {file.name}
            </p>
            <button className='remove-button' onClick={() => handleRemoveFile(index)}>
              Remove  
            </button>
          </div>
        ))}

      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Condition;
