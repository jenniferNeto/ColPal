import React from 'react'
import { useAuth } from '../../context/UserContext'
import PipelineCard from './PipelineCard'

export default function Dashboard() {
    const {currentUser} = useAuth()

    return (
        <div className='bg-white d-flex shadow flex-column h-100 p-3 rounded'>
            <div className=' mb-4'>
                <h2>Welcome, {currentUser['username']}</h2>
            </div>
            <div className='row'>
            {
                [0,1,2,4,5,6,7,8,9].map(id => (
                    <div className='col-md-4 col-sm-12 my-3'>
                        <PipelineCard id={id} />
                    </div>
                ))
            }

</div>
        </div>
    )
}
