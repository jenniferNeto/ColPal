import React, { useEffect } from 'react'
import { get_user_pipelines } from '../utils/endpoints'

import Dashboard from '../components/home/Dashboard'
import MessageQueue from '../components/home/MessageQueue'
import { useAuth } from '../context/UserContext'
import useRequest from '../hooks/useRequest'

export default function HomePage() {
  const { currentUser } = useAuth()

  const { 
    response: pipelines, 
    doRequest: userPipelinesRequest
  } = useRequest(get_user_pipelines(currentUser['id']))

  useEffect(() => {
    userPipelinesRequest()
  }, [userPipelinesRequest])


  return (
    <div className='row py-2 h-100'>
      <div className='col-sm-9'>
        <Dashboard pipelines={pipelines?.data}/>
      </div>
      <div className='col-sm-3'>
        <MessageQueue />
      </div>

    </div>
  )
}
