
import {parseFrequency} from "../../utils/functions";
import { useNavigate } from "react-router-dom";
import Pill from "../commons/Pill";

export default function PipelineCard({data}) {
  const {id, title, is_stable, approved, upload_frequency} = data;
  const navigate = useNavigate();
  const [day, hours, minutes, seconds] = parseFrequency(upload_frequency);
  
  return (
   
      <div className='py-4 px-3 bg-main-100 rounded-xl cursor-pointer' onClick={() => navigate("/pipeline/"+id, {state: {data}})}>
          <div className="flex justify-between mb-3">
            <span className="font-bold">{title}</span> 
            <div>
              <Pill text={is_stable ? 'stable': 'unstable'} color={is_stable ? 'emerald-500':'red-500'} />
              <Pill text={approved ? 'approved': 'unapproved'} color={approved ? 'emerald-500':'red-500'} />
            </div>
          </div>

          <hr className='my-2' />

          <div className='flex justify-between'>
            <span>Upload Frequency:</span> <span>{`${day}d ${hours}h ${minutes}m  ${seconds}s `}</span>
          </div>
      </div>
  
  )
}
