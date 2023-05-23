import React from 'react'
import NotificationCard from './NotifcationCard'
import Panel from '../commons/Panel'
export default function MessageQueue({notifications}) {
    if (notifications === null)
        return

    return (
        <Panel>

            <div className='text-3xl font-bold mb-4'>
                <h2>Notifications</h2>
            </div>
            <hr />
            <div className='scroll' style={{maxHeight: '85vh'}}>
            {
                notifications.slice(0).reverse().map(notification => (
                    <div key={notification.id} className='col-md-12 col-sm-12 my-3'>
                        <NotificationCard data={notification}/>
                    </div>
                ))
            }
            </div>
        </Panel>
    )
}
