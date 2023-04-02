import {useState, useEffect} from 'react'
import { useParams, useLocation } from "react-router-dom";
import { post_pipeline_file } from '../utils/endpoints'
import axios from 'axios'

import PipelineUpload from '../components/pipelines/PipelineUpload';
import PipelineHistory from '../components/pipelines/PipelineHistory';
import PipelineChangeLog from '../components/pipelines/PipelineChangeLog';
import PipelineTimeTrack from "../components/pipelines/PipelineTimeTrack"
import useRequest from '../hooks/useRequest';
import UploadCheckout from '../components/file-upload/UploadCheckout';

export default function Pipeline() {
  const { state } = useLocation();

  const [uploadedFile, setUploadedFile] = useState(null)
  const [showCheckout, setShowCheckout] = useState(false)
  const [uploadHistory, setUploadHistory] = useState([])

  const uploadRequest = useRequest(post_pipeline_file(state.data.id))
  
 
  const handleFileUpload = (file) => {
    setUploadedFile(file)
    setShowCheckout(true)
  }

  const handleFileCheckout = async () => { 
    await uploadRequest.doRequest({'file': uploadedFile})
    setShowCheckout(false)
  }

  //Getiing the history of the pipeline from mock data
  useEffect(() => {
    const get_history = async () => {
      const res = await axios.get('/mock-data/pipeline_uploads.json');
      setUploadHistory(res.data)
    }
    get_history()
  }, [])

  useEffect(() => {
    if (uploadRequest.response) {
      console.log(uploadRequest.response)
    }
  }, [uploadRequest.response])

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
            <PipelineHistory uploadHistory={uploadHistory}/>
          </div>
          <div className='col-sm-12 mt-3 h-25'>
            <PipelineChangeLog />
          </div>
        </div>
        <div className="col-sm-3">
          <PipelineTimeTrack frequency={state.data.upload_frequency}/>
        </div>
      </div>
    </>
  )
}
