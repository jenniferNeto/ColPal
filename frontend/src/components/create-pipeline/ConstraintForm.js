import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileUpload } from '@fortawesome/free-solid-svg-icons'

export default function ConstraintForm() {

    const [columnName, setColumnName] = useState('')
    const [columnType, setColumnType] = useState('')

    const [constraints, setConstraints] = useState([])

    const addConstraint = () => {
        if (!columnName || !columnType) return; // Needs both column name and type
        if (constraints.find(c => c.columnName === columnName)) return; // Column name must be unique
        setConstraints([...constraints, { columnName, columnType }])
    }

    const removeConstraint = (index) => {
        setConstraints(constraints.filter((_, i) => i !== index))
    }

    const editConstraint = (index, columnName, columnType) => {
        setConstraints(constraints.map((c, i) => i === index ? { columnName, columnType } : c))
    }

    return (
        <div className='card shadow'>
            <div className='card-header'>
                <div class="d-grid gap-2">
                    <label className="m-0 mr-2 upload-btn" style={{ border: '3px dashed #605CA8' }}>
                        <FontAwesomeIcon icon={faFileUpload} /> Load Template File
                    </label>
                </div>
            </div>

            <div className='card-body'>
                <div className="row">
                    <div className="col-sm-5">
                        <input type="text" class="form-control" placeholder="Column Name" onChange={e => setColumnName(e.target.value)} />
                    </div>
                    <div className="col-sm-5">
                        <select className='form-control' onChange={e => setColumnType(e.target.value)}>
                            <option value={"None"}>Column Type</option>
                            <option value={"Varchar"}>String</option>
                            <option value={"Integer"}>Integer</option>
                            <option value={"Float"}>Float</option>
                            <option value={"Date"}>Date</option>
                            <option value={"Datetime"}>Datetime</option>
                            <option value={"Email"}>Email</option>
                            <option value={"Boolean"}>Boolean</option>

                        </select>
                    </div>
                    <div className="col-sm-1">
                        <button className="btn btn-sm btn-success" onClick={addConstraint}>Add</button>
                    </div>
                </div>

                {constraints.map(({ columnName, columnType }, index) => (
                    <div className="row my-1" key={index}>
                        <div className="col-sm-5">
                            <input type="text" class="form-control" value={columnName} 
                            onChange={(e) => editConstraint(index, e.target.value, columnType)}/>
                        </div>
                        <div className="col-sm-5">
                            <select className='form-control' value={columnType}
                            onChange={(e) => editConstraint(index, columnName, e.target.value)}>
                                <option value={"None"}>Column Type</option>
                                <option value={"Varchar"}>String</option>
                                <option value={"Integer"}>Integer</option>
                                <option value={"Float"}>Float</option>
                                <option value={"Date"}>Date</option>
                                <option value={"Datetime"}>Datetime</option>
                                <option value={"Email"}>Email</option>
                                <option value={"Boolean"}>Boolean</option>

                            </select>
                        </div>
                        <div className="col-sm-1">
                            <button className="btn btn-sm btn-danger" onClick={(e) => removeConstraint(index)}>Remove</button>
                        </div>


                    </div>

                ))}
            </div>
        </div>
    )
}
