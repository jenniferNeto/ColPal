import React, {useEffect} from 'react'

import Dashboard from '../components/home/Dashboard'
import MessageQueue from '../components/home/MessageQueue'

import { getUserPipelines } from '../api/users'
import { useAuth } from '../context/UserContext'
export default function HomePage() {
  
  const {currentUser} = useAuth()

  useEffect(() => {
    getUserPipelines(currentUser['id']).then(res => {
      console.log(res)
    })
  })

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
