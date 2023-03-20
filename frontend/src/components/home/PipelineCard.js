import React from 'react'
import { useNavigate } from "react-router-dom";

export default function PipelineCard({id, title, is_active, upload_frequency}) {
  const navigate = useNavigate();

  return (
   
      <div className='card' style={{border: 'none', background: '#E9E7FD', cursor: "pointer"}} 
      onClick={() => navigate("/pipeline/"+id)}>
          <div className='card-body'>
          <div class="card-title align-center d-flex justify-content-between">
            <h5>{title}</h5> <span className={`dot ${is_active ? 'active': 'inactive'}`}></span>
          </div>
          </div>
          <div className='card-footer'>
            {upload_frequency}
          </div>
      </div>
  
  )
}
