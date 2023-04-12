import { useState } from 'react'
import FormSelect from 'react-bootstrap/esm/FormSelect'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileUpload } from '@fortawesome/free-solid-svg-icons'

export default function ConstraintForm() {

    const [columnName, setColumnName] = useState('')
    const [columnType, setColumnType] = useState('')

    const [constraints, setConstraints] = useState([])

    const addConstraint = () => {
        if (!columnName || !columnType) return;
        if (constraints.find(c => c.columnName === columnName)) return;
        setConstraints([...constraints, { columnName, columnType }])
    }
    
    const removeConstraint = (index) => {
        setConstraints(constraints.filter((_, i) => i !== index))
    }



    return (
        <div class="d-grid gap-2">
            <label className="m-0 mr-2 upload-btn" style={{ border: '3px dashed #605CA8' }}>
                <FontAwesomeIcon icon={faFileUpload} /> Load Template File

            </label>
            <div className="row">

                <div className="col-sm-5">
                    <input type="text" class="form-control" placeholder="Column Name" onChange={e => setColumnName(e.target.value)} />
                </div>
                <div className="col-sm-5">
                    <FormSelect onChange={e => setColumnType(e.target.value)}>
                        <option value={"None"}>Column Type</option>
                        <option value={"Varchar"}>String</option>
                        <option value={"Integer"}>Integer</option>
                        <option value={"Float"}>Float</option>
                        <option value={"Date"}>Date</option>
                        <option value={"Datetime"}>Datetime</option>
                        <option value={"Email"}>Email</option>
                        <option value={"Boolean"}>Boolean</option>

                    </FormSelect>
                </div>
                <div className="col-sm-1">
                    <button className="btn btn-success" onClick={addConstraint}>Add</button>
                </div>


            </div>

            {constraints.map(({columnName, columnType}, index) => (
                <div className="row">
                    <div className="col-sm-5">
                        <input type="text" class="form-control" disabled value={columnName} />
                    </div>
                    <div className="col-sm-5">
                        <input type="text" class="form-control" disabled value={columnType}  />
                    </div>
                    <div className="col-sm-1">
                        <button className="btn btn-danger" onClick={() => removeConstraint(index)}>Remove</button>
                    </div>


                </div>

            ))}
        </div>
    )
}
