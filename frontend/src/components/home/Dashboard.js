import React from 'react'
import { useAuth } from '../../context/UserContext'
import PipelineCard from './PipelineCard'
import Spinner from 'react-bootstrap/Spinner';

export default function Dashboard({pipelines}) {
    const {currentUser} = useAuth()
    console.log(pipelines)

    if (pipelines === null) {
        return (
            <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
            </Spinner>
        )
    }

    return (
        
        <div className='bg-white d-flex shadow flex-column h-100 p-3 rounded'>
            <div className=' mb-4'>
                <h2>Welcome, {currentUser['username']}</h2>
            </div>
            <div className='row'>
            {
                pipelines.map(pipeline => (
                    <div key={pipeline.id} className='col-md-4 col-sm-12 my-3'>
                        <PipelineCard {...pipeline}/>
                    </div>
                ))
            }

</div>
        </div>
    )
}
