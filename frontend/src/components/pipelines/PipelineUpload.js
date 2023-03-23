import React from 'react'
import { faFileUpload } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

export default function PipelineUpload() {

  const handleUpload = () => {
    console.log(e)
  }

  return (
    <div class="card shadow-sm bg-white h-100">
      <div className='card-body'>
        <h4>Upload File</h4>
      </div>
      <div className='card-footer'>
      <div class="d-grid gap-2">
        <label className="m-0 mr-2 upload-btn" style={{border: '3px dashed #605CA8'}}>
          <FontAwesomeIcon icon={faFileUpload} /> Upload
          <input
            type="file"
            onChange={handleUpload}
            style={{ opacity: 0, position: "absolute", left: "-9999px" }}
          />
        </label>
        </div>
      </div>
    </div>
  )
}
