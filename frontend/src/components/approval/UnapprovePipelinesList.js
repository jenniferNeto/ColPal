import {formatDate} from '../../utils/functions'

export default function UnapprovedPipelinesList({pipelines, onSelect}) {

  return (
    
        <table className="min-w-full text-left max-h-96 overflow-y-scroll">
          <thead className='border-b dark:border-neutral-500'>
            <tr>
              <th scope="col" className='p-3'>ID</th>
              <th scope="col" className='p-3'>Title</th>
              <th scope="col" className='p-3'>Upload Frequency</th>
              <th scope="col" className='p-3'>Hard Deadline</th>
              <th scope="col" className='p-3'>Created</th>
              <th scope="col" className='p-3'>Select</th>
            </tr>
          </thead>
          <tbody>
            {pipelines.map((pipeline) => (
                <tr className="border-b dark:border-neutral-500">
                  <th scope="row" className='whitespace-nowrap p-3'>{pipeline.id}</th>
                  <td scope='row' className='whitespace-nowrap p-3'>{pipeline.title}</td>
                  <td scope='row' className='whitespace-nowrap p-3'>{pipeline.upload_frequency}</td>
                  <td scope='row' className='whitespace-nowrap p-3'>{String(pipeline.hard_deadline)}</td>
                  <td scope='row' className='whitespace-nowrap p-3'>{formatDate(pipeline.created)}</td>
                  <td scope='row' className='whitespace-nowrap p-3'>
                      <button className='bg-emerald-500 hover:bg-emerald-700 text-white py-1 px-2 rounded' onClick={() => onSelect(pipeline)}>Approve</button>
                  </td>
               </tr>
            ))}
         

          </tbody>
        </table>
    
  )
}
