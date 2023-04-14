
import {parseFrequency} from "../../utils/functions";
import { useNavigate } from "react-router-dom";

export default function PipelineCard({data}) {
  const {id, title, is_stable, approved, upload_frequency} = data;
  const navigate = useNavigate();
  const [day, hours, minutes, seconds] = parseFrequency(upload_frequency);
  
  return (
   
      <div className='card' style={{border: 'none', background: '#E9E7FD', cursor: "pointer"}} 
      onClick={() => navigate("/pipeline/"+id, {state: {data}})}>
          <div className='card-body'>
          <div className="card-title d-flex justify-content-between">
            <h5>{title}</h5> 
            <div>
            <span className={`badge me-1 rounded-pill bg-${is_stable ? 'success': 'danger'}`}>
              {is_stable ? 'stable': 'unstable'}</span>
            <span className={`badge rounded-pill bg-${approved ? 'success': 'danger'}`}>
              {approved ? 'approved': 'not approved'}</span>
            </div>
              
          </div>
          </div>
          <div className='card-footer d-flex justify-content-between'>
            <span>Upload Frequency:</span> <span>{`${day}d ${hours}h ${minutes}m  ${seconds}s `}</span>
          </div>
      </div>
  
  )
}
