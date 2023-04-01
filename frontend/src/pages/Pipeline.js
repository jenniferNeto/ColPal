import { useState } from 'react'
import { useParams } from "react-router-dom";
import { post_pipeline_file } from '../utils/endpoints'
import PipelineUpload from '../components/pipelines/PipelineUpload';
import PipelineHistory from '../components/pipelines/PipelineHistory';
import PipelineChangeLog from '../components/pipelines/PipelineChangeLog';
import PipelineTimeTrack from "../components/pipelines/PipelineTimeTrack"
import useRequest from '../hooks/useRequest';
import UploadCheckout from '../components/file-upload/UploadCheckout';

export default function Pipeline() {
  const params = useParams()
  const [uploadedFile, setUploadedFile] = useState(null)
  const [showCheckout, setShowCheckout] = useState(false)
  const uploadRequest = useRequest(post_pipeline_file(params['pipeline_id']))

  const handleFileUpload = (file) => {
    setUploadedFile(file)
    setShowCheckout(true)
  }

  const handleFileCheckout = async () => { 

    await uploadRequest.doRequest({'file': uploadedFile})
    setShowCheckout(false)
  }

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
            <PipelineHistory />
          </div>
          <div className='col-sm-12 h-25'>
            <PipelineChangeLog />
          </div>
        </div>
        <div className="col-sm-3">
          <PipelineTimeTrack />
        </div>
      </div>
    </>
  )
}
