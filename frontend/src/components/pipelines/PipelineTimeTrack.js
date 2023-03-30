import React from 'react'
import CountdownTimer from '../commons/CountdownTimer'
export default function PipelineTimeTrack() {
  const date = new Date('2023-03-30T00:00:00')
  return (
    <div class="card shadow-sm bg-white h-100">
      <CountdownTimer duration={60000} />
    </div>
  )
}
