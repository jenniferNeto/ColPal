import React from 'react'
import Card from 'react-bootstrap/Card'
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
              {[...Array(20).keys()].map((row) => (
                <tr>
                  <td scope="col">File Name</td>
                  <td scope="col">Upload Date</td>
                  <td scope="col">View</td>

                </tr>
              ))}

            </tbody>
          </table>
        </Card.Body>
    </Card>
  )
}
