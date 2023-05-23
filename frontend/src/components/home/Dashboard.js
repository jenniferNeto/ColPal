import Panel from '../commons/Panel';
import { useAuth } from '../../context/UserContext'
import PipelineCard from './PipelineCard'
import Spinner from 'react-bootstrap/Spinner';

export default function Dashboard({ pipelines }) {
    const { currentUser } = useAuth()
    console.log(pipelines)

    if (pipelines === null) {
        return (
            <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
            </Spinner>
        )
    }

    return (

        <Panel>
            <div className='text-3xl font-bold mb-4'>
                <h2>Welcome, {currentUser['username']}</h2>
            </div>
            <hr />
            <div className='row'>
                {
                    pipelines.map(pipeline => (
                        <div key={pipeline.id} className='col-md-4 col-sm-12 my-3'>
                            <PipelineCard data={pipeline} />
                        </div>
                    ))
                }

            </div>
        </Panel>
    )
}
