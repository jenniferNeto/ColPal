import { useEffect, useMemo } from 'react'
import useRequest from '../../hooks/useRequest'
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/esm/Button';
import ConstraintTable from '../create-pipeline/ConstraintTable'
import { put_approve_pipeline, get_pipeline_constraints } from '../../utils/endpoints'

export default function PipelinesApproveCheckout({selected, show, close}) {

  const approvePipeReq = useRequest(put_approve_pipeline(selected.id))
  const constraintPipeReq = useRequest(get_pipeline_constraints(selected.id))

  const handleCheckout = async () => {
    await approvePipeReq.doRequest({"approved": true})
    close()
  }

  useEffect(() => {
    constraintPipeReq.doRequest()
  }, [constraintPipeReq.doRequest])

  const constraints = useMemo(() => constraintPipeReq.response?.data ?? [], [constraintPipeReq.response])

  return (
    <Modal show={show}  onHide={close}>
      <Modal.Header closeButton>
        <Modal.Title>Approve {selected.title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
      <div className='shadow-sm card h-100'>
        <div className='card-body scroll'>
          <ConstraintTable constraints={constraints} />
        </div>

      </div>
        
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={close}>
          Go Back
        </Button>
        <Button variant="primary" onClick={handleCheckout}>
            Confirm
        </Button>
      </Modal.Footer>
    </Modal>

  )
}
