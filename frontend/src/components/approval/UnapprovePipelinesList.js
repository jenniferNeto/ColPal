import {formatDate} from '../../utils/functions'

export default function UnapprovedPipelinesList({pipelines, onSelect}) {

  return (
    <div className='shadow-sm card h-100'>
      <div className='card-header'><h4>Unapproved Pipelines</h4></div>
      <div className='card-body scroll'>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Title</th>
              <th scope="col">Upload Frequency</th>
              <th scope="col">Hard Deadline</th>
              <th scope="col">Created</th>
              <th scope="col">Select</th>
            </tr>
          </thead>
          <tbody>
            {pipelines.map((pipeline) => (
                <tr>
                  <th scope="row">{pipeline.id}</th>
                  <td>{pipeline.title}</td>
                  <td>{pipeline.upload_frequency}</td>
                  <td>{String(pipeline.hard_deadline)}</td>
                  <td>{formatDate(pipeline.created)}</td>
                  <td>
                      <button className='btn btn-sm btn-success' onClick={() => onSelect(pipeline)}>Approve</button>
                  </td>
               </tr>
            ))}
         

          </tbody>
        </table>
      </div>
    </div>
    
  )
}
