import React from 'react'
import { useNavigate } from "react-router-dom";

export default function PipelineCard({id, title, is_active, upload_frequency}) {
  const navigate = useNavigate();

  return (
   
      <div className='card' style={{border: 'none', background: '#E9E7FD', cursor: "pointer"}} 
      onClick={() => navigate("/pipeline/"+id)}>
          <div className='card-body'>
          <div className="card-title align-center d-flex justify-content-between">
            <h5>{title}</h5> <span className={`dot ${is_active ? 'active': 'inactive'}`}></span>
          </div>
          </div>
          <div className='card-footer d-flex justify-content-between'>
            <span>Next Upload:</span> <span>{upload_frequency}</span>
          </div>
      </div>
  
  )
}
