import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import React from 'react'
import Card from 'react-bootstrap/Card'
import { faEye } from "@fortawesome/free-solid-svg-icons"
export default function PipelineHistory() {
  return (
    <Card className="shadow-sm bg-white h-100">
        <Card.Body className='scroll'>
          <table className="table" >
            <thead>
              <tr>
                <th scope="col">File Name</th>
                <th scope="col">Upload Date</th>
                <th scope="col">View</th>

              </tr>
            </thead>
            <tbody>
              {[...Array(5).keys()].map((row) => (
                <tr>
                  <td scope="col">File {row}</td>
                  <td scope="col">____</td>
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
