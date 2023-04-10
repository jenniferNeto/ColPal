import React from 'react'
import useParser from '../../hooks/useParser'
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

export default function CSVDisplay({csv}) {
const { columns, rows } = useParser(csv)
  return (
    <div className="container-fluid px-0">
    <div className="row g-0 h-100">
      <div className="col-lg-12 border vh-50">
        <table className="table" >
          <thead>
            <tr>
              <th scope="col">#</th>
              {columns && columns.map((col) => <th scope="col">{col}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows && rows.map((row, index) => (
              <tr>
                <th scope="row">{index}</th>
                {columns.map(col=> <td scope="col">{row[col] ?? '___'}</td>)}
              </tr>
            ))}

          </tbody>
        </table>
      </div>

    </div>
  </div>
  )
}

export const CSVModal = ({ show, file, close }) => {

  return (
    <Modal show={show} fullscreen={true} onHide={close}>
      <Modal.Header closeButton>
        <Modal.Title>{file && file.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>

      <CSVDisplay csv={file} />
        
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={close}>
          Go Back
        </Button>
      </Modal.Footer>
    </Modal>
  )
}
