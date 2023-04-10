import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faFileUpload } from "@fortawesome/free-solid-svg-icons"

export default function PipelineCreate() {
  return (
    <div className="row h-100">

      <div className='col-sm-12 card shadow bg-white p-2'>
        <h4 className='card-header p-3'>Create a New Pipeline</h4>
        <div className='card-body'>
          <form>
            <div class="form-group">
              <label for="formGroupExampleInput">Example label</label>
              <input type="text" class="form-control" id="formGroupExampleInput" placeholder="Example input" />
            </div>
            <div class="form-group">
              <label for="formGroupExampleInput2">Another label</label>
              <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Another input" />
            </div>
          </form>
        </div>

      </div>

      <div className='col-sm-12 card shadow bg-white p-2 mt-3'>

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
