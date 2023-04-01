import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import Card from 'react-bootstrap/Card'
import { faEye } from "@fortawesome/free-solid-svg-icons"
import axios from 'axios'

export default function PipelineHistory({uploadHistory}) {
 
  return (
    <Card className="shadow-sm bg-white h-100">
        <Card.Body className='scroll'>
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
                  <td scope="col">{upload['filename']}</td>
                  <td scope="col">{upload['upload_time']}</td>
                  <td scope="col">
                    <FontAwesomeIcon icon={faEye} className="view-btn" />
                  </td>

                </tr>
              ))}

            </tbody>
          </table>
        </Card.Body>
    </Card>
  )
}
