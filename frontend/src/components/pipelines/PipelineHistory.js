import {useState} from 'react'
import axios from 'axios'
import { formatDate } from '../../utils/functions'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import Card from 'react-bootstrap/Card'
import { faEye } from "@fortawesome/free-solid-svg-icons"
import {CSVModal} from '../commons/CSVDisplay'

export default function PipelineHistory({uploadHistory}) {
  const [showModal, setShowModal] = useState(false)
  const [viewFile, setViewFile] = useState(null)

  const handleOpen = async (fileURL) => {
      const baseUrl = "https://storage.cloud.google.com/colgate-data-storage/"
      const fileName = fileURL.split("/").pop()
      try {
          const config = { responseType: 'blob', maxRedirects: 0 };
          const res = await axios.get(baseUrl+fileURL, config)
          setViewFile(new File([res.data], fileName))  
          setShowModal(true)
      } catch (err) {
          console.log(err)
      } 

    
  }

  const handleClose = () => {
    setViewFile(null)
    setShowModal(false)
  }

  return (
    <>
    {viewFile && <CSVModal show={showModal} file={viewFile} close={handleClose}/>}
    <Card className="shadow bg-white h-100">
        <Card.Body className='scroll '>
          <table className="table" >
            <thead>
              <tr>
                <th scope="col">File Name</th>
                <th scope="col">Upload Time</th>
                <th scope="col">View</th>

              </tr>
            </thead>
            <tbody>
              {uploadHistory.map((upload) => (
                <tr>
                  <td scope="col">{upload['path'].split("/").pop()}</td>
                  <td scope="col">{formatDate(upload['upload_date'])}</td>
                  <td scope="col">
                    <FontAwesomeIcon icon={faEye} className="view-btn" onClick={() => handleOpen(upload['path'])}/>
                  </td>

                </tr>
              ))}

            </tbody>
          </table>
        </Card.Body>
    </Card>
    </>
  )
}
