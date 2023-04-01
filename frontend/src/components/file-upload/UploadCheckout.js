import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import useParser from '../../hooks/useParser';
import CSVDisplay from '../commons/CSVDisplay';
export default function UploadCheckout({ show, file, checkout, close }) {

  if (!file) return null

  return (
    <Modal show={show} fullscreen={true} onHide={close}>
      <Modal.Header closeButton>
        <Modal.Title>{file.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>

      <CSVDisplay csv={file} />
        
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={close}>
          Go Back
        </Button>
        <Button variant="primary" onClick={checkout}>
          Checkout Upload
        </Button>
      </Modal.Footer>
    </Modal>
  )
}
