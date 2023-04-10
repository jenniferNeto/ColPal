import {useState} from 'react'
import { faFileUpload } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

export default function PipelineUpload({upload}) {

  const [file, setFile] = useState("")
  const [fileIntput, setFileInput] = useState("")
  
  const handleFileSelect = (e) => {
    const uploadedFile = e.target.files[0]
    setFile(uploadedFile)
    //TBD: Add file size check
    //TBD: Add file type check (csv only)
    //TBB: Add file name check

  }

  const handleFileConfirm = () => {
    upload(file)
    setFileInput("")
    setFile(null)
  }

  const handleFileCancel = () => {
    setFileInput("")
    setFile(null)
  }


  return (
    <div class="card shadow bg-white">
      <div className='card-body'>
        {file ? (
          <div className='d-flex justify-content-between'>
            <p className='m-0 lead'>{file.name}</p>
            <span>
            <button className="btn btn-sm btn-success mx-2" onClick={handleFileConfirm}>
              Confirm
            </button>
            <button className="btn btn-sm btn-danger" onClick={handleFileCancel}>
              Cancel
            </button>
            </span>
          </div>
        ) : (
        <p className='m-1 lead'>No file selected</p>
        )}
        </div>
      
      <div className='card-footer'>
  
      <div class="d-grid gap-2">
        <label className="m-0 mr-2 upload-btn" style={{border: '3px dashed #605CA8'}}>
          <FontAwesomeIcon icon={faFileUpload} /> Upload
          <input
            type="file" 
            value={fileIntput}
            onChange={handleFileSelect}
            style={{ opacity: 0, position: "absolute", left: "-9999px" }}
          />
        </label>
        </div>
      </div>
    </div>
  )
}
