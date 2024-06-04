import React, { useState } from 'react';

function TssMasterTable() {
     const [ file, setFile ] = useState(null);

     const handleFileUpload = (e) => {
        const selectedFile = Array.from(e.target.file);
    
        
        
      };

      return (

        <div className="form-group">
        <label>Upload Replicates:</label>
        <input
          type="file"
          onChange={handleFileUpload}
          accept=".tsv"
        />
        </div>

      );
}

export default TssMasterTable;