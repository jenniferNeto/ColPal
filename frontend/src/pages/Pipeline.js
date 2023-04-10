import {useState, useEffect, useMemo} from 'react'
import { useLocation, useParams } from "react-router-dom";
import { post_pipeline_file, get_pipeline_uploads, get_pipeline_due_date } from '../utils/endpoints'

import PipelineUpload from '../components/pipelines/PipelineUpload';
import PipelineHistory from '../components/pipelines/PipelineHistory';
import PipelineChangeLog from '../components/pipelines/PipelineChangeLog';
import PipelineTimeTrack from "../components/pipelines/PipelineTimeTrack"
import useRequest from '../hooks/useRequest';
import UploadCheckout from '../components/file-upload/UploadCheckout';

export default function Pipeline() {
  const {pipeline_id} = useParams();

  const [uploadedFile, setUploadedFile] = useState(null)
  const [showCheckout, setShowCheckout] = useState(false)

  const uploadRequest = useRequest(post_pipeline_file(pipeline_id))
  const fileHistoryRequest = useRequest(get_pipeline_uploads(pipeline_id))
  const dueDateRequest = useRequest(get_pipeline_due_date(pipeline_id))
  
 
  const handleFileUpload = (file) => {
    setUploadedFile(file)
    setShowCheckout(true)
  }

  const handleFileCheckout = async () => { 
    await uploadRequest.doRequest({'file': uploadedFile})
    await dueDateRequest.doRequest()
    setUploadedFile(null)
    setShowCheckout(false)
  }

  //Getiing the history of the pipeline
  useEffect(() => {

    fileHistoryRequest.doRequest()
    dueDateRequest.doRequest()
   
  }, [uploadRequest.response, fileHistoryRequest.doRequest])

  const pipelineFileHistory = useMemo(() => fileHistoryRequest.response?.data ?? [],
    [fileHistoryRequest.response]
  )

  const nextDueDate = useMemo(() => dueDateRequest.response?.data ?? null,
    [dueDateRequest.response]
  )

  return (
    <>
      <UploadCheckout show={showCheckout}
        file={uploadedFile}
        checkout={handleFileCheckout}
        close={() => setShowCheckout(false)} />
        
      <div className='row h-100'>
        <div className="row col-sm-9">
          <div className='col-sm-12 h-25'>
            <PipelineUpload upload={handleFileUpload} />
          </div>
          <div className='col-sm-12 h-50'>
            <PipelineHistory uploadHistory={pipelineFileHistory}/>
          </div>
          <div className='col-sm-12 mt-3 h-25'>
            <PipelineChangeLog />
          </div>
        </div>
        <div className="col-sm-3">
          <PipelineTimeTrack dueDate={nextDueDate}/>
        </div>
      </div>
    </>
  )
}
