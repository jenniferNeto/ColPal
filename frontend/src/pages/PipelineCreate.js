
import Panel from "../components/commons/Panel";
import { useState } from "react";
import useRequest from "../hooks/useRequest";
import { post_pipeline_create } from "../utils/endpoints";

import ConstraintForm from "../components/create-pipeline/ConstraintForm";
import ConstraintTable from "../components/create-pipeline/ConstraintTable";

export default function PipelineCreate() {
  const [title, setTitle] = useState('');
  const [frequency, setFrequency] = useState('');
  const [hardDeadline, setHardDeadline] = useState(false)
  const [constraints, setConstraints] = useState([])
  const pipelineCreateRequest = useRequest(post_pipeline_create())


  const handlePipelineCreate = async (e) => {
    e.preventDefault();

    await pipelineCreateRequest.doRequest({
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

  return (
    <div className="h-100">

      <div className="max-h-full">

        <Panel>
          <form onSubmit={handlePipelineCreate}>
            <div className="grid md:grid-cols-12 gap-4 mt-2 mb-4">
              <div className="md:col-span-5 sm:col-span-12">
                <input type="text" class="form-control" placeholder="Pipeline Title" value={title} onChange={(e) => setTitle(e.target.value)} />
              </div>
              <div className="md:col-span-4 sm:col-span-12">
                <input type="text" class="form-control" placeholder="Upload Frequency" value={frequency} onChange={(e) => setFrequency(e.target.value)} />
              </div>
              <div className="md:col-span-2 sm:col-span-6">
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
              <div className="md:col-span-1 sm:col-span-6">
                <button type="submit" className="bg-emerald-500 hover:bg-emerald-700 text-white py-2 px-4 rounded">Create</button>
              </div>
            </div>

            <div className="m-2 max-h-48 overflow-y-scroll overflow-x-hidden">
              <ConstraintTable constraints={constraints} />
            </div>

          </form>
        </Panel>

      </div>


      <div className="max-h-full">
        <ConstraintForm onSave={constraints => setConstraints(constraints)} />
      </div>

    </div>

  )
}
