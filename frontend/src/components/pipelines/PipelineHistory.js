import { useState } from 'react'
import { formatDate } from '../../utils/functions'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import Card from 'react-bootstrap/Card'
import { faEye } from "@fortawesome/free-solid-svg-icons"
import { CSVModal } from '../commons/CSVDisplay'
import Panel from '../commons/Panel'

export default function PipelineHistory({ uploadHistory }) {
  const [showModal, setShowModal] = useState(false)
  const [viewFile, setViewFile] = useState(null)

  /*
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

  }*/

  const handleClose = () => {
    setViewFile(null)
    setShowModal(false)
  }

  return (
   
      <Panel>
        {viewFile && <CSVModal show={showModal} file={viewFile} close={handleClose} />}
        <table className="table max-h-full overflow-y-scroll" >
          <thead>
            <tr>
              <th scope="col">File Name</th>
              <th scope="col">Upload Time</th>
              <th scope="col">Download</th>

            </tr>
          </thead>
          <tbody>
            {uploadHistory.map((upload) => (
              <tr>
                <td scope="row">{upload['path'].split("/").pop()}</td>
                <td scope="row">{formatDate(upload['upload_date'])}</td>
                <td scope="row">
                  <a href={"https://storage.cloud.google.com/dataplatformcolgate_cloudbuild/" + upload['path']}>
                    <FontAwesomeIcon icon={faEye} className="view-btn" />
                  </a>
                </td>

              </tr>
            ))}

          </tbody>
        </table>
      </Panel>
 
  )
}
