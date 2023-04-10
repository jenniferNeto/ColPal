import CountdownTimer from '../commons/CountdownTimer'

export default function PipelineTimeTrack({dueDate}) {

  if(!dueDate) return null;

  return (
    <div class="card shadow bg-white h-100 text-center p-2">
      <h4>Next Upload Due:</h4>
      <CountdownTimer startDate={dueDate.last_upload} endDate={dueDate.next_upload} />
    </div>
  )
}
