import {useState} from 'react'
import { faFileUpload } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import Panel from '../commons/Panel'

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
    <Panel>

        {file ? (
          <div className='flex justify-between'>
            <p className='m-0'>{file.name}</p>
            <span>
            <button className="bg-emerald-500 hover:bg-emerald-700 text-white py-1 px-2 rounded mx-1" onClick={handleFileConfirm}> 
              Confirm
            </button>
            <button className="bg-red-500 hover:bg-red-700 text-white py-1 px-2 rounded mx-1" onClick={handleFileCancel}>
              Cancel
            </button>
            </span>
          </div>
        ) : (
        <p className='m-1'>No file selected</p>
        )}
    
      
      <hr className='my-2' />
  
      <div class="grid gap-2">
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

    </Panel>
  )
}
