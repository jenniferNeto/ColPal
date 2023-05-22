
import {parseFrequency} from "../../utils/functions";
import { useNavigate } from "react-router-dom";

export default function PipelineCard({data}) {
  const {id, title, is_stable, approved, upload_frequency} = data;
  const navigate = useNavigate();
  const [day, hours, minutes, seconds] = parseFrequency(upload_frequency);
  
  return (
   
      <div className='py-4 px-3 bg-main-100 rounded-xl cursor-pointer' onClick={() => navigate("/pipeline/"+id, {state: {data}})}>
          <div className="flex justify-between mb-3">
            <span className="font-bold">{title}</span> 
            <div>
              <span className={`bg-${is_stable ? 'emerald':'red'}-500 inline-block rounded-full px-2 py-1 mx-1 text-sm font-semibold text-white`}>
                {is_stable ? 'stable': 'unstable'}
              </span>
              <span className={`bg-${approved ? 'emerald':'red'}-500 inline-block rounded-full px-2 py-1 mx-1 text-sm font-semibold text-white`}>
                {approved ? 'approved': 'unapproved'}
              </span>
            </div>
          </div>

          <hr className='my-2' />

          <div className='flex justify-between'>
            <span>Upload Frequency:</span> <span>{`${day}d ${hours}h ${minutes}m  ${seconds}s `}</span>
          </div>
      </div>
  
  )
}
