import React from 'react'
import { useParams } from "react-router-dom";
import FileUpload from '../components/pipelines/FileUpload';
import FileHistory from '../components/pipelines/FileHistory';

export default function Pipeline() {
  const params = useParams()

  console.log(params)
  return (
    <div className='row h-100'>
      <div className='col-sm-12'>
        <FileUpload />
      </div>
      <div className='col-sm-12 h-50'>
        <FileHistory />
      </div>
    </div>
  )
}
