import React, { useEffect } from 'react'
import { getAllUserPipelines } from '../utils/endpoints'

import Dashboard from '../components/home/Dashboard'
import MessageQueue from '../components/home/MessageQueue'
import { useAuth } from '../context/UserContext'
import useRequest from '../hooks/useRequest'

export default function HomePage() {
  const { currentUser } = useAuth()

  const { 
    response: pipelines, 
    doRequest: getUserPipelines
  } = useRequest(`/pipelines/user/${currentUser['id']}/`)

  useEffect(() => {
    getUserPipelines()
  }, [getUserPipelines])


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
