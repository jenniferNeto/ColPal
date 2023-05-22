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
      <div className='border border-grey-300 rounded-sm h-100'>
        <div className='overflow-y-auto max-h-fit'>
          <ConstraintTable constraints={constraints} />
        </div>

      </div>
        
      </Modal.Body>
      <Modal.Footer>
        <button className='bg-red-500 hover:bg-red-700 text-white py-2 px-4 rounded' onClick={close}>Go Back</button>
        <button className='bg-emerald-500 hover:bg-emerald-700 text-white py-2 px-4 rounded' onClick={handleCheckout}>Confirm</button>

      </Modal.Footer>
    </Modal>

  )
}
