import React from 'react'
import { useParams } from "react-router-dom";
import PipelineUpload from '../components/pipelines/PipelineUpload';
import PipelineHistory from '../components/pipelines/PipelineHistory';
import PipelineChangeLog from '../components/pipelines/PipelineChangeLog';
import PipelineTimeTrack from "../components/pipelines/PipelineTimeTrack"
export default function Pipeline() {
  const params = useParams()

  console.log(params)
  return (
    <div className='row h-100'>
      <div className="row col-sm-8">
        <div className='col-sm-12 h-25'>
          <PipelineUpload />
        </div>
        <div className='col-sm-12 py-2 h-50'>
          <PipelineHistory />
        </div>
        <div className='col-sm-12 h-25'>
          <PipelineChangeLog />
        </div>
      </div>
      <div className="col-sm-4">
      <PipelineTimeTrack />
      </div>
    </div>
  )
}
