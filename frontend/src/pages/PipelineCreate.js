import { useState } from "react";
import useRequest from "../hooks/useRequest";
import { post_pipeline_create } from "../utils/endpoints";

import ConstraintForm from "../components/create-pipeline/ConstraintForm";
import UserRoleForm from "../components/create-pipeline/UserRoleForm";

export default function PipelineCreate() {
  const [title, setTitle] = useState('');
  const [frequency, setFrequency] = useState('');
  const [hardDeadline, setHardDeadline] = useState(false)
  const [constraints, setConstraints] = useState([])
  const pipelineCreateReq = useRequest(post_pipeline_create())

  const handlePipelineCreate = async (e) => {
    e.preventDefault();

    await pipelineCreateReq.doRequest({ 
      title, 
      "upload_frequency": frequency, 
      "hard_deadline": hardDeadline, 
      constraints
    })

    setTitle('')
    setFrequency('')
    setHardDeadline(false)
    setConstraints([])
  }

  console.log(constraints)

  return (
    <div className="h-100">

      <div className="card shadow col-sm-12 mb-2">
        <div className="card-body">
          <form onSubmit={handlePipelineCreate}>
            <div className="row my-2">
              <div className="col-sm-5">
                <input type="text" class="form-control" placeholder="Pipeline Title" value={title} onChange={(e) => setTitle(e.target.value)} />
              </div>
              <div className="col-sm-4">
                <input type="text" class="form-control" placeholder="Upload Frequency" value={frequency} onChange={(e) => setFrequency(e.target.value)} />
              </div>
              <div className="col-sm-2">
                <div class="form-check">
                  <input class="form-check-input"
                    id="flexCheckIndeterminate"
                    type="checkbox"
                    checked={hardDeadline}
                    onChange={e => setHardDeadline(e.target.checked)}
                  />
                  <label class="form-check-label" for="flexCheckIndeterminate">
                    Hard Deadline
                  </label>
                </div>
              </div>
              <div className="col-sm-1">
                <input type="submit" class="btn btn-primary" />
              </div>
            </div>
            <div className="row m-2">
           
                <table>
                  <thead>
                    <tr>
                      <th>Column Name</th>
                      <th scope="col">Column Type</th>
                    </tr>
                  </thead>
                  <tbody>
                    {constraints.map(({column_name, column_type}) => (
                      <tr>
                        <th scope="row">{column_name}</th>
                        <td>{column_type}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
    
            </div>
          </form>
        </div>
      </div>


      <div className="row">

        <div className="col-sm-6">
          <UserRoleForm />
        </div>

        <div className="col-sm-6" style={{ maxHeight: '85%' }}>
          <ConstraintForm onSave={constr => setConstraints(constr)} />
        </div>

      </div>


    </div>

  )
}
