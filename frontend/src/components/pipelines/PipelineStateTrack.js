import CountdownTimer from '../commons/CountdownTimer'
import { getDuration } from '../../utils/functions';

export default function PipelineStateTrack({nextDeadline, state}) {

  if(!nextDeadline) return null;

  return (
    <div class="card shadow bg-white h-100 text-center p-2">
      <h4>Next Upload Due:</h4>
      <CountdownTimer 
        track={state.approved} 
        deadline={nextDeadline} 
        total={getDuration(state.upload_frequency)}
      />
    </div>
  )
}
