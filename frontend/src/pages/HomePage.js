import React, { useEffect, useMemo } from 'react'
import { get_user_pipelines, get_user_notifications } from '../utils/endpoints'

import Dashboard from '../components/home/Dashboard'
import MessageQueue from '../components/home/MessageQueue'
import { useAuth } from '../context/UserContext'
import useRequest from '../hooks/useRequest'

export default function HomePage() {
  const { currentUser } = useAuth()

  const { 
    response: pipelinesRes, 
    doRequest: userPipelinesRequest
  } = useRequest(get_user_pipelines(currentUser['id']))

  const { 
    response: userRes, 
    doRequest: userNotificationRequest
  } = useRequest(get_user_notifications(currentUser['id']))

  const pipelines = useMemo(() => pipelinesRes?.data ?? null,
    [pipelinesRes]
  )

  const notifications = useMemo(() => userRes?.data ?? null,
  [userRes]
)

  useEffect(() => {
    userPipelinesRequest()
  }, [userPipelinesRequest])

  useEffect(() => {
    userNotificationRequest()
  }, [userNotificationRequest])


  return (
    
    <div className='row py-2 h-100'>
      <div className='col-sm-9'>
        <Dashboard pipelines={pipelines}/>
      </div>
      <div className='col-sm-3'>
        <MessageQueue notifications={notifications} />
      </div>

    </div>
  )
}
