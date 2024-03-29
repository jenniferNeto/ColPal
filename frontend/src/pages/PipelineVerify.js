import { useEffect, useState, useMemo } from 'react'
import { useAuth } from '../context/UserContext'
import { useNavigate } from 'react-router-dom';
import useRequest from '../hooks/useRequest'
import { get_unapproved_pipelines } from '../utils/endpoints'
import UnapprovedPipelinesList from '../components/approval/UnapprovePipelinesList'
import PipelinesApproveCheckout from '../components/approval/PipelinesApproveCheckout'
import Panel from '../components/commons/Panel'

export default function PipelineVerify() {
  const [selectedPipeline, setSelectedPipeline] = useState(null)
  const [showApprove, setShowApprove] = useState(false)
  const { currentUser } = useAuth()
  const navigate = useNavigate()

  const unapprovedPipesReq = useRequest(get_unapproved_pipelines())

  const handleClose = () => {
    unapprovedPipesReq.doRequest()
    setShowApprove(false)
    setSelectedPipeline(null)
  }

  const handleOpen = (pipeline) => {
    setSelectedPipeline(pipeline)
    setShowApprove(true)

  }

  useEffect(() => {

    if (!currentUser.admin) navigate("/")

    unapprovedPipesReq.doRequest()
  }, [unapprovedPipesReq.doRequest])

  const pipelines = useMemo(() => unapprovedPipesReq.response?.data ?? [], [unapprovedPipesReq.response])

  return (
    <div className='h-5/6'>
      {selectedPipeline && <PipelinesApproveCheckout selected={selectedPipeline} show={showApprove} close={handleClose} />}
      <Panel>
        <UnapprovedPipelinesList pipelines={pipelines} onSelect={(pipeline) => handleOpen(pipeline)} />
      </Panel>

    </div>
  )
}
