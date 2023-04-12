import {useState } from "react";

import ConstraintForm from "../components/create-pipeline/ConstraintForm";
import UserRoleList from "../components/create-pipeline/UserRoleList";

export default function PipelineCreate() {
  const [title, setTitle] = useState('');
  const [frequency, setFrequency] = useState('');
  const [stable, setStable] = useState(true);

 

  return (

      <div className='card shadow bg-white h-100'>

        <div className="card-header">
          <h5>Create a New Pipeline</h5>
        </div>

        <div className="card-body row">

          <form className="col-sm-6 border-end border-2">
            <div className="row">
              <div class="col-sm-6 my-2">
                <input type="text" class="form-control" placeholder="Pipeline Title" onChange={(e) => setTitle(e.target.value)} />
              </div>
              <div class="col-sm-6 my-2">
                <input type="text" class="form-control" placeholder="Upload Frequency" onChange={(e) => setFrequency(e.target.value)} />
              </div>
              <hr />
              <div class="col-sm-12">
                <UserRoleList />
              </div>
            </div>
          </form>

          <div className="col-sm-6">
            <ConstraintForm />
          </div>

        </div>


      </div>

  )
}
