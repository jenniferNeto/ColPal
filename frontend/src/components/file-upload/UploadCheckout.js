import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import useParser from '../../hooks/useParser';
export default function UploadCheckout({ show, file, checkout, close }) {

  const { columns, rows } = useParser(file)

  if (!file) return null

  return (
    <Modal show={show} fullscreen={true} onHide={close}>
      <Modal.Header closeButton>
        <Modal.Title>{file.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>

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
