import React from 'react'
import { Link } from 'react-router-dom'
export default function PipelineCard({id, title,upload_frequency}) {

  return (
    <Link to={"/pipeline/"+id}>
      <div className='card' style={{border: 'none', background: '#E9E7FD'}} >
          <div className='card-body'>
          <h5 class="card-title align-center">{title}</h5>
          </div>
          <div className='card-footer'>
            {upload_frequency}
          </div>
      </div>
    </Link>
  )
}
