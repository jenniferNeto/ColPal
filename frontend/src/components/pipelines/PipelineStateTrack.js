import CountdownTimer from '../commons/CountdownTimer'
import { getDuration } from '../../utils/functions';
import Panel from '../commons/Panel';
export default function PipelineStateTrack({nextDeadline, state}) {

  if(!nextDeadline) return null;

  return (
    <Panel>
      <p className='text-bold text-center mb-2'>Next Upload Due:</p>
      <CountdownTimer 
        track={state.approved} 
        deadline={nextDeadline} 
        total={getDuration(state.upload_frequency)}
      />
    </Panel>
  )
}
