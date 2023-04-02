import {getDuration} from '../../utils/functions'
import CountdownTimer from '../commons/CountdownTimer'
export default function PipelineTimeTrack({frequency}) {
  
  const duration = getDuration(frequency)
  
  return (
    <div class="card shadow-sm bg-white h-100 text-center p-2">
      <h4>Next Upload Due:</h4>
      <CountdownTimer duration={duration} />
    </div>
  )
}
