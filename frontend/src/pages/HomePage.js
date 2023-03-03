import React from 'react'

import Dashboard from '../components/home/Dashboard'
import MessageQueue from '../components/home/MessageQueue'
export default function HomePage() {
  return (
    <div className='row py-2 h-100'>
      <div className='col-sm-9'>
        <Dashboard />
      </div>
      <div className='col-sm-3'>
        <MessageQueue />
      </div>
      
    </div>  
  )
}
