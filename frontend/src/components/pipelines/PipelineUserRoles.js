import { useMemo, useState, useEffect } from "react";
import useRequest from '../../hooks/useRequest';
import { get_all_users, get_pipeline_roles } from "../../utils/endpoints";
import { useAuth } from "../../context/UserContext";

export default function PipelineUserRoles({pipelineId}) {

    const [selectedUser, setSelectedUser] = useState('')
    const [selectedRole, setSelectedRole] = useState('')

    const allUsersRequest = useRequest(get_all_users())
    const managersRequest = useRequest(get_pipeline_roles(pipelineId, 'managers'))
    const uploadersRequest = useRequest(get_pipeline_roles(pipelineId, 'uploaders'))
    const viewersRequest = useRequest(get_pipeline_roles(pipelineId, 'viewers'))

    const {currentUser} = useAuth()

    const addUserRole = () => {
        console.log(selectedUser)
        console.log(selectedRole)
    }

    useEffect(() => {
        allUsersRequest.doRequest()

        managersRequest.doRequest()
        uploadersRequest.doRequest()
        viewersRequest.doRequest()

    }, [allUsersRequest.doRequest, managersRequest.doRequest, uploadersRequest.doRequest, viewersRequest.doRequest])


    const users = useMemo(() => allUsersRequest.response?.data ?? [], [allUsersRequest.response])

    return (
        <div className="card shadow">
            <div className="card-header">
                
    
            </div>

           
        <div className='card-body'>
        <table className="table" >
            <thead>
              <tr>
                <th scope="col">User</th>
                <th scope="col">Role</th>
                <th scope="col">Remove</th>
              </tr>
            </thead>
            <tbody>
            {[].map(({ username, role }, index) => (
                <tr>
                <td scope="col">user</td>
                <td scope="col">role</td>
                <td scope="col">
                  X
                </td>

              </tr>
            ))}

            </tbody>
          </table>
        </div>
        {currentUser.admin && (
            <div className='card-footer'>
            <div class="form-group row">
                        <div className="col-sm-4">
                            <select className="form-control" onChange={e => setSelectedUser(e.target.value)}>
                                <option>Select Users</option>
                                {users.map(user => <option key={user['id']} value={user['name']}>{user['username']}</option>)}
                            </select>
                        </div>
                        <div className="col-sm-5">
                            <select className='form-control' onChange={e => setSelectedRole(e.target.value)}>
                                <option disabled value={"None"}>Select Role</option>
                                <option value={"viewers"}>Viewer</option>
                                <option value={"uploaders"}>Uploader</option>
                                <option value={"managers"}>Manager</option>
                            </select>
                          
                        </div>
                        <div className="col-sm-3">
                            <button className="btn btn-primary" onClick={addUserRole}>Add User</button>
                        </div>
                    </div>
            </div>
        )}
        
    </div>
    )
}
