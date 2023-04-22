import { useEffect, useMemo } from 'react';

import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import CSVDisplay from '../commons/CSVDisplay';
import useRequest from '../../hooks/useRequest';
import { post_pipeline_file } from '../../utils/endpoints';

export default function UploadCheckout({ show, file, checkout, validationErrors, close }) {

  if (!file) return null
  console.log(Object.values(validationErrors))
  return (
    <Modal show={show} fullscreen={true} onHide={close}>
      <Modal.Header closeButton>
        <Modal.Title>{file.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>

        <CSVDisplay csv={file} />
         { Object.values(validationErrors).map(({col, row, error}) => (
            <p>{row}:{col} {error}</p>
          ))}
      
        
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
