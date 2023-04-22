import { useMemo, useState, useEffect } from "react";
import useRequest from '../../hooks/useRequest';
import { get_all_users, get_pipeline_roles, add_pipeline_role, delete_pipeline_roles } from "../../utils/endpoints";
import { useAuth } from "../../context/UserContext";

export default function PipelineUserRoles({ pipelineId }) {

    const [selectedUser, setSelectedUser] = useState('')
    const [selectedRole, setSelectedRole] = useState('')

    const allUsersRequest = useRequest(get_all_users())

    const managersRequest = useRequest(get_pipeline_roles(pipelineId, 'managers'))
    const uploadersRequest = useRequest(get_pipeline_roles(pipelineId, 'uploaders'))
    const viewersRequest = useRequest(get_pipeline_roles(pipelineId, 'viewers'))

    const addManagerRequest = useRequest(add_pipeline_role(pipelineId, 'managers'))
    const addUploaderRequest = useRequest(add_pipeline_role(pipelineId, 'uploaders'))
    const addViewerRequest = useRequest(add_pipeline_role(pipelineId, 'viewers'))

    const deleteManagerRequest = useRequest(add_pipeline_role(pipelineId, 'managers'))
    const deleteUploaderRequest = useRequest(add_pipeline_role(pipelineId, 'uploaders'))
    const deleteViewerRequest = useRequest(add_pipeline_role(pipelineId, 'viewers'))

    const { currentUser } = useAuth()

    const handleAddUserRole = async () => {
        switch (selectedRole) {
            case 'managers':
                return addManagerRequest.doRequest({ 'id': selectedUser })
            case 'uploaders':
                return addUploaderRequest.doRequest({ 'id': selectedUser })
            case 'viewers':
                return addViewerRequest.doRequest({ 'id': selectedUser })
            default:
                break
        }
        
        setSelectedRole('')
        setSelectedUser('')
    }

    useEffect(() => {
        allUsersRequest.doRequest()

        managersRequest.doRequest()
        uploadersRequest.doRequest()
        viewersRequest.doRequest()

    }, [addManagerRequest.response, addUploaderRequest.response, addViewerRequest.response])

    const userRoles = useMemo(() => {
        let userRoles = {[currentUser.id]: { 'username': currentUser.username, 'roles': ['viewer'] }}
        const managers = managersRequest.response?.data ?? []
        const uploaders = uploadersRequest.response?.data ?? []
        const viewers = viewersRequest.response?.data ?? []

        managers.forEach((user) => userRoles[user.id] = { 'username': user.username, 'roles': ['manager'] })
        uploaders.forEach((user) => userRoles[user.id] ?
            userRoles[user.id]['roles'].push('uploader') :
            userRoles[user.id] = {
                'username': user.username, 'roles': ['uploader']
            })
        viewers.forEach((user) => {
            userRoles[user.id] ?
            userRoles[user.id]['roles'].push('viewer') :
            userRoles[user.id] = { 'username': user.username, 'roles': ['viewer'] }
        })

        return userRoles

    }, [managersRequest.response, uploadersRequest.response, viewersRequest.response])

    const users = useMemo(() => allUsersRequest.response?.data ?? [], [allUsersRequest.response])

    console.log(userRoles)
    return (
        <div className="card shadow">
            <div className='card-body scroll py-1'>
                <table className="table" >
                    <thead>
                        <tr>
                            <th scope="col">User</th>
                            <th scope="col">Role</th>
                            <th scope="col">Remove</th>
                        </tr>
                    </thead>
                    <tbody>
                        
                        <tr>
                            <td scope="col"><b>{userRoles[currentUser.id].username}</b> <em>(you)</em></td>
                            <td scope="col">{userRoles[currentUser.id].roles.map(role => <span class="badge bg-primary me-1">{role}</span>)}</td>
                            <td scope="col">_____________</td>
                        </tr>

                        {Object.entries(userRoles).map(([id, user]) => (
                            currentUser.id != id && (
                                <tr key={id}>
                                    <td scope="col"><b>{user.username}</b></td>
                                    <td scope="col">{user.roles.map(role => <span class="badge bg-primary me-1">{role}</span>)}</td>
                                    <td scope="col">
                                        <select className='form-control' onChange={e => setSelectedRole(e.target.value)}>
                                            <option disabled value={""}>Remove Role</option>
                                            {user.roles.map(role => <option value={role}>{role}</option>)}
                                           
                                        </select>
                                    </td>

                                </tr>
                            )
                        ))}

                    </tbody>
                </table>
            </div>
            {(currentUser.admin || userRoles[currentUser.id].roles.includes('manager')) && (
                <div className='card-footer'>
                    <div class="form-group row">
                        <div className="col-sm-4">
                            <select className="form-control" onChange={e => setSelectedUser(e.target.value)}>
                                <option>Select Users</option>
                                {users.map(user => <option key={user['id']} value={user['id']}>{user['username']}</option>)}
                            </select>
                        </div>
                        <div className="col-sm-5">
                            <select className='form-control' onChange={e => setSelectedRole(e.target.value)}>
                                <option disabled value={""}>Select Role</option>
                                <option value={"viewers"}>Viewer</option>
                                <option value={"uploaders"}>Uploader</option>
                                <option value={"managers"}>Manager</option>
                            </select>

                        </div>
                        <div className="col-sm-3">
                            <button className="btn btn-primary" onClick={handleAddUserRole}>Add User</button>
                        </div>
                    </div>
                </div>
            )}

        </div>
    )
}
