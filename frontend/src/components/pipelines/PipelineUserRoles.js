import { useMemo, useState, useEffect } from "react";
import useRequest from '../../hooks/useRequest';
import { get_all_users, get_pipeline_roles, add_pipeline_role, delete_pipeline_roles } from "../../utils/endpoints";
import { useAuth } from "../../context/UserContext";
import Panel from "../commons/Panel";
import Pill from "../commons/Pill";

export default function PipelineUserRoles({ pipelineId }) {

    const [selectedUser, setSelectedUser] = useState('')
    const [selectedRole, setSelectedRole] = useState('viewers')

    const allUsersRequest = useRequest(get_all_users())

    const managersRequest = useRequest(get_pipeline_roles(pipelineId, 'managers'))
    const uploadersRequest = useRequest(get_pipeline_roles(pipelineId, 'uploaders'))
    const viewersRequest = useRequest(get_pipeline_roles(pipelineId, 'viewers'))

    const addManagerRequest = useRequest(add_pipeline_role(pipelineId, 'managers'))
    const addUploaderRequest = useRequest(add_pipeline_role(pipelineId, 'uploaders'))
    const addViewerRequest = useRequest(add_pipeline_role(pipelineId, 'viewers'))

    const deleteManagerRequest = useRequest(delete_pipeline_roles(pipelineId, 'managers'))
    const deleteUploaderRequest = useRequest(delete_pipeline_roles(pipelineId, 'uploaders'))
    const deleteViewerRequest = useRequest(delete_pipeline_roles(pipelineId, 'viewers'))

    const { currentUser } = useAuth()

    const handleAddUserRole = async () => {
        console.log(selectedRole, selectedUser)
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

    const handleRemoveRole = async (e, userId) => {
        e.preventDefault()
        const data = new FormData(e.target);
        const role = data.get('role')

        switch (role) {
            case 'manager':
                return deleteManagerRequest.doRequest({ 'id': userId })
            case 'uploader':
                return deleteUploaderRequest.doRequest({ 'id': userId })
            case 'viewer':
                return deleteViewerRequest.doRequest({ 'id': userId })
            default:
                break
        }
    }

    useEffect(() => {
        allUsersRequest.doRequest()

        managersRequest.doRequest()
        uploadersRequest.doRequest()
        viewersRequest.doRequest()

    }, [addManagerRequest.response, addUploaderRequest.response, addViewerRequest.response,
    deleteViewerRequest.response, deleteUploaderRequest.response, deleteManagerRequest.response
    ])

    const userRoles = useMemo(() => {
        let userRoles = { [currentUser.id]: { 'username': currentUser.username, 'roles': ['viewer'] } }

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

    return (
        <Panel>
            <table className="table max-h-full overflow-y-scroll" >
                <thead>
                    <tr>
                        <th scope="col">User</th>
                        <th scope="col">Role</th>
                        <th scope="col">Remove</th>
                    </tr>
                </thead>
                <tbody>

                    <tr>
                        <td scope="row"><b>{userRoles[currentUser.id].username}</b> <em>(you)</em></td>
                        <td scope="row">{userRoles[currentUser.id].roles.map(role => <Pill text={role} color='main-500' />)}</td>
                        <td scope="row">__________</td>
                    </tr>

                    {Object.entries(userRoles).map(([id, user]) => (
                        currentUser.id != id && (
                            <tr key={id}>
                                <td scope="row"><b>{user.username}</b></td>
                                <td scope="row">{user.roles.map(role => <Pill text={role} color='main-500' />)}</td>
                                <td scope="row">
                                    <form className="input-group" method="POST" onSubmit={(e) => handleRemoveRole(e, id)}>
                                        <select className='form-control form-control-sm' name="role">
                                            <option disabled value={""}>Remove Role</option>
                                            {user.roles.map(role => <option value={role}>{role}</option>)}

                                        </select>
                                        <button className="btn btn-sm btn-danger">Remove</button>
                                    </form>
                                </td>

                            </tr>
                        )
                    ))}

                </tbody>
            </table>
        
            {(currentUser.admin || userRoles[currentUser.id].roles.includes('manager')) && (
                    <div className="grid gap-3 grid-cols-12 my-2 ">
                        <div className="col-span-4">
                            <select className="form-control" onChange={e => setSelectedUser(e.target.value)}>
                                <option>Select Users</option>
                                {users.map(user => <option key={user['id']} value={user['id']}>{user['username']}</option>)}
                            </select>
                        </div>
                        <div className="col-span-6">
                            <select className='form-control' onChange={e => setSelectedRole(e.target.value)}>
                                <option disabled value={""}>Select Role</option>
                                <option value={"viewers"}>Viewer</option>
                                <option value={"uploaders"}>Uploader</option>
                                <option value={"managers"}>Manager</option>
                            </select>

                        </div>
                        <div className="col-span-2">
                            <button className="bg-emerald-500 hover:bg-emerald-700 text-white py-2 px-4 rounded w-100" onClick={handleAddUserRole}>Add User</button>
                        </div>
                    </div>
           
            )}

        </Panel>
    )
}
