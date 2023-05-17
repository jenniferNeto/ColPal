
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
              <span className={`inline-block rounded-full px-2 py-1 mx-1 text-sm font-semibold text-white`} style={{background: is_stable ? '#50C878': '#FF00000'}}>
                {is_stable ? 'stable': 'unstable'}
              </span>
              <span className={`inline-block bg-${approved ? 'green': 'red'}-500 rounded-full px-2 py-1 mx-1 text-sm font-semibold text-white`} style={{background: approved ? '#50C878': 'red'}}>
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
