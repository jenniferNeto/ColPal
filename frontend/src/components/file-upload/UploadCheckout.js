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
        <button className='bg-red-500 hover:bg-red-700 text-white py-2 px-4 rounded' onClick={close}>Go Back</button>
        <button className='bg-emerald-500 hover:bg-emerald-700 text-white py-2 px-4 rounded' onClick={checkout}>Checkout Upload</button>
      </Modal.Footer>
    </Modal>
  )
}
