import Panel from '../commons/Panel'
import { useEffect, useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileUpload } from '@fortawesome/free-solid-svg-icons'
import useRequest from '../../hooks/useRequest'
import { post_create_constraints } from '../../utils/endpoints'

export default function ConstraintForm({ onSave }) {

    const [columnName, setColumnName] = useState('')
    const [columnType, setColumnType] = useState('')
    const [constraints, setConstraints] = useState([])

    const createConstraintRequest = useRequest(post_create_constraints())

    const handleFileSelect = async (file) => {
        await createConstraintRequest.doRequest({ 'file': file })
    }



    const addConstraint = () => {
        if (!columnName || !columnType) return; // Needs both column name and type
        if (constraints.find(c => c.columnName === columnName)) return; // Column name must be unique
        setConstraints([...constraints, { "column_name": columnName, "column_type": columnType }])
    }

    const removeConstraint = (index) => {
        setConstraints(constraints.filter((_, i) => i !== index))
    }

    const editConstraint = (index, columnName, columnType) => {
        setConstraints(constraints.map((c, i) => i === index ? { columnName, columnType } : c))
    }

    const saveConstraints = () => {
        for (let i = 0; i < constraints.length; i++) {
            if (!constraints[i].column_name || !constraints[i].column_type) {
                alert("All constraints must have a column name and type")
                return;
            }
        }

        onSave(constraints)
    }

    useEffect(() => {
        setConstraints((createConstraintRequest.response?.data["constraints"] ?? []))
    }, [createConstraintRequest.response])

    return (
        <Panel>
            <div class="grid gap-2">
                <label className="mr-2 upload-btn" >
                    <FontAwesomeIcon icon={faFileUpload} /> Load Template File
                    <input
                        type="file"
                        onChange={e => handleFileSelect(e.target.files[0])}
                        style={{ opacity: 0, position: "absolute", left: "-9999px" }}
                    />
                </label>
            </div>



            <div className="mx-auto grid md:grid-cols-3 gap-3 my-4 max-h-72 overflow-y-scroll overflow-x-hidden">
                <div>
                    <input type="text" class="form-control" placeholder="Column Name" onChange={e => setColumnName(e.target.value)} />
                </div>
                <div>
                    <select className='form-control' onChange={e => setColumnType(e.target.value)}>
                        <option value={"None"}>Column Type</option>
                        <option value={"str"}>String</option>
                        <option value={"int"}>Integer</option>
                        <option value={"float"}>Float</option>
                        <option value={"date"}>Date</option>
                        <option value={"address"}>Address</option>
                        <option value={"email"}>Email</option>
                        <option value={"bool"}>Boolean</option>

                    </select>
                </div>
                <div>
                    <button className="bg-emerald-500 hover:bg-emerald-700 text-white py-2 px-3 rounded" onClick={addConstraint}>Add</button>
                </div>


                {constraints.map(({ column_name, column_type }, index) => (
                    <>
                        <div>
                            <input type="text" class="form-control" value={column_name}
                                onChange={(e) => editConstraint(index, e.target.value, column_type)} />
                        </div>
                        <div>
                            <select className='form-control' value={column_type}
                                onChange={(e) => editConstraint(index, column_name, e.target.value)}>
                                <option disabled value={"None"}>Column Type</option>
                                <option value={"str"}>String</option>
                                <option value={"int"}>Integer</option>
                                <option value={"float"}>Float</option>
                                <option value={"date"}>Date</option>
                                <option value={"address"}>Address</option>
                                <option value={"email"}>Email</option>
                                <option value={"bool"}>Boolean</option>
                            </select>
                        </div>
                        <div>
                            <button className="bg-red-500 hover:bg-red-700 text-white py-2 px-3 rounded" onClick={(e) => removeConstraint(index)}>Remove</button>
                        </div>

                    </>

                ))}

            </div>





            <button className="bg-blue-500 hover:bg-blue-700 text-white py-2 px-3 rounded w-100 disabled:opacity-25" onClick={saveConstraints} disabled={!constraints.length}>Save Constraints</button>


        </Panel>
    )
}
