import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faFileUpload } from "@fortawesome/free-solid-svg-icons"

export default function PipelineCreate() {
  return (
    <div className="row h-100">

      <div className='card shadow bg-white h-25'>
        
        <div className="card-header">
          <h5>Create a New Pipeline</h5>
        </div>

        <div className="card-body">
          <form>
            <div className="row">
              <div class="col-sm-6 my-1">
                <input type="text" class="form-control" placeholder="Pipeline Title" />
              </div>
              <div class="col-sm-6 my-1">
                <input type="text" class="form-control" placeholder="Upload Frequency" />
              </div>
              <div class="col-sm-12 my-1">
                <input type="text" class="form-control" placeholder="Upload Frequency" />
              </div>
            </div>
          </form>
        </div>

      </div>

      <div className='col-sm-12 card shadow bg-white p-2 mt-3 h-75'>

        <div className='card-header'>
          <div class="d-grid gap-2">
            <label className="m-0 mr-2 upload-btn" style={{ border: '3px dashed #605CA8' }}>
              <FontAwesomeIcon icon={faFileUpload} /> Load Template File
             
            </label>
          </div>
        </div>

        <div className='card-body h-100'>


        </div>
      </div>
    </div>
  )
}
