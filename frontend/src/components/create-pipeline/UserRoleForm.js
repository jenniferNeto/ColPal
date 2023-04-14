import { useMemo, useState, useEffect } from "react";
import useRequest from '../../hooks/useRequest';
import { get_all_users } from "../../utils/endpoints";
import FormSelect from "react-bootstrap/esm/FormSelect";

export default function UserRoleForm() {
    const [userRoles, setUserRoles] = useState([]);
    const [selectedUser, setSelectedUser] = useState('')
    
    const [isManager, setIsManager] = useState(false)
    const [isViewer, setIsViewer] = useState(false)
    const [isUploader, setIsUploader] = useState(false)

    const allUsersRequest = useRequest(get_all_users())

    const addSelectedUser = () => {
        if(!isManager && !isViewer && !isUploader) return  //Needs at least one role
        setUserRoles([...userRoles, selectedUser])
    }

    useEffect(() => {
        allUsersRequest.doRequest()
    }, [allUsersRequest.doRequest])


    const users = useMemo(() => allUsersRequest.response?.data ?? [], [allUsersRequest.response])
    return (
        <div className="card shadow h-100">
            <div className="form-inline card-header">
                <div class="form-group mb-2">
                    <select className="form-control" onChange={e => setSelectedUser(e.target.value)}>
                        <option>Select Users</option>
                        {users.map(user =>
                        <option key={user['id']} value={user['username']}>{user['username']}</option>)
                        }
                    </select>
                    <button className="btn btn-primary">Add User Role</button>
                </div>
            </div>
        </div>
    )
}
