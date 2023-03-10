import React, { useState, useEffect } from 'react'
import { getAllPipelines } from '../../api/pipelines'
import { useAuth } from '../../context/UserContext'
import PipelineCard from './PipelineCard'

export default function Dashboard() {
    const {currentUser} = useAuth()
    const [pipelines, setPipelines] = useState([])
    useEffect(() => {
        const fetchPipelines = async () => {
            const res = await getAllPipelines()
            setPipelines(res.data)
        }
        fetchPipelines()
    }, [])
    return (
        <div className='bg-white d-flex shadow flex-column h-100 p-3 rounded'>
            <div className=' mb-4'>
                <h2>Welcome, {currentUser['username']}</h2>
            </div>
            <div className='row'>
            {
                pipelines.map(data => (
                    <div className='col-md-4 col-sm-12 my-3'>
                        <PipelineCard data={data} />
                    </div>
                ))
            }

</div>
        </div>
    )
}
