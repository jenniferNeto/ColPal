import { useState, useEffect, useMemo } from 'react'
import { useAuth } from '../context/UserContext';
import { useLocation, useParams, useNavigate } from "react-router-dom";
import { post_pipeline_file, get_pipeline_uploads, get_pipeline_deadline, get_pipeline_roles } from '../utils/endpoints'

import PipelineUpload from '../components/pipelines/PipelineUpload';
import PipelineHistory from '../components/pipelines/PipelineHistory';

import PipelineStateTrack from "../components/pipelines/PipelineStateTrack"
import PipelineUserRoles from '../components/pipelines/PipelineUserRoles';

import useRequest from '../hooks/useRequest';
import UploadCheckout from '../components/file-upload/UploadCheckout';

export default function Pipeline() {

  const { pipeline_id } = useParams();
  const { state } = useLocation()
  const navigate = useNavigate()

  const [uploadedFile, setUploadedFile] = useState(null)
  const [showCheckout, setShowCheckout] = useState(false)

  const { currentUser } = useAuth()
  const [showRoles, setShowRoles] = useState(false)
  const [showUpload, setShowUpload] = useState(false)

  const uploadRequest = useRequest(post_pipeline_file(pipeline_id))
  const fileHistoryRequest = useRequest(get_pipeline_uploads(pipeline_id))
  const deadlineRequest = useRequest(get_pipeline_deadline(pipeline_id))

  const managersRequest = useRequest(get_pipeline_roles(pipeline_id, 'managers'))
  const uploadersRequest = useRequest(get_pipeline_roles(pipeline_id, 'uploaders'))


  const handleFileUpload = (file) => {
    setUploadedFile(file)
    setShowCheckout(true)
    uploadRequest.invalidate()
  }

  const handleFileCheckout = async () => {
    await uploadRequest.doRequest({ 'file': uploadedFile })
  }


  useEffect(() => {
    if (uploadRequest.response) navigate(0)

    managersRequest.doRequest()
    uploadersRequest.doRequest()
    deadlineRequest.doRequest()
    fileHistoryRequest.doRequest()

  }, [uploadRequest.response, fileHistoryRequest.doRequest, deadlineRequest.doRequest])

  useEffect(() => {
    const managers = managersRequest.response?.data ?? []
    const uploaders = uploadersRequest.response?.data ?? []

    const isManager = managers.some(manager => manager.id == currentUser.id)
    const isUploader = uploaders.some(uploader => uploader.id == currentUser.id)

    console.log(isManager, isUploader)

    setShowRoles(isManager)
    setShowUpload(isUploader)
  }, [managersRequest.response, uploadersRequest.response, currentUser.id])


  const pipelineFileHistory = useMemo(() => fileHistoryRequest.response?.data ?? [],
    [fileHistoryRequest.response]
  )

  const nextDeadline = useMemo(() => deadlineRequest.response?.data.deadline ?? null,
    [deadlineRequest.response]
  )

  const validationErrors = useMemo(() => uploadRequest.error?.response.data ?? [],
    [uploadRequest.error]
  )

  const historyHeight = useMemo(() => {
    let historyHeight = 100
    let uploadHeight = 25
    let rolesHeight = 30
    if (showRoles) historyHeight -= rolesHeight
    if (showUpload) historyHeight -= uploadHeight
    return `${historyHeight}%`
  }, [showUpload, showRoles, managersRequest.response, uploadersRequest.response])


  return (
    <div className="grid md:grid-cols-4 sm:grid-cols-1 gap-2 h-full">
      
      <UploadCheckout show={showCheckout}
            validationErrors={validationErrors}
            file={uploadedFile}
            checkout={handleFileCheckout}
            close={() => setShowCheckout(false)} />
    

      <div className='col-span-3 h-full'>
      
        {showUpload && <div><PipelineUpload upload={handleFileUpload} /></div>}

        <div className="my-2" style={{ height: historyHeight }}>
          <PipelineHistory uploadHistory={pipelineFileHistory} />
        </div>

        {showRoles && <div><PipelineUserRoles pipelineId={pipeline_id} /></div>}

      </div>

     
        <PipelineStateTrack
          state={state.data}
          nextDeadline={nextDeadline}
        />
   

    </div>
  )
}
