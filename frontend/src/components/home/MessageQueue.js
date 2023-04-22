import React from 'react'
import NotificationCard from './NotifcationCard'

export default function MessageQueue({notifications}) {
    if (notifications === null)
        return

    return (
        <div className='bg-white d-flex shadow flex-column h-100 p-3 rounded'>
            <h2>Notifications</h2>
            <hr />
            <div className='col'>
            {
                notifications.map(notification => (
                    <div key={notification.id} className='col-md-12 col-sm-12 my-3'>
                        <NotificationCard data={notification}/>
                    </div>
                ))
            }
            </div>
        </div>
    )
}
