import React from 'react'
import { faUpload } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
export default function PipelineUpload({onFileSelect}) {
  const handleFileInput = (e) => {
    // handle validations
    onFileSelect(e.target.files[0])
}

  return (
    <div class="card p-3 shadow-sm bg-white h-100">
      <h2>File Upload</h2>
      
      <button className='btn btn-lg' 
      style={{'border': '3px dotted #605CA8', 'color': '#605CA8' }}>
        <FontAwesomeIcon icon={faUpload} className="me-2"/>  
        <input type="file" onChange={handleFileInput}/> 
      </button>
     
      
    </div>
  )
}
