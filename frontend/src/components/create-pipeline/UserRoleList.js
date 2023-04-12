import { useMemo, useState, useEffect } from "react";
import useRequest from '../../hooks/useRequest';
import { get_all_users } from "../../utils/endpoints";
import FormSelect from "react-bootstrap/esm/FormSelect";

export default function UserRoleList() {
    const [userRoles, setUserRoles] = useState([]);
    const [selectedUser, setSelectedUser] = useState('')
    
    const [isManager, setIsManager] = useState(false)
    const [isViewer, setIsViewer] = useState(false)
    const [isUploader, setIsUploader] = useState(false)

    const allUsersRequest = useRequest(get_all_users())

    const addSelectedUser = () => {
        
        setUserRoles([...userRoles, selectedUser])
    }

    useEffect(() => {
        allUsersRequest.doRequest()
    }, [allUsersRequest.doRequest])


    const users = useMemo(() => allUsersRequest.response?.data ?? [], [allUsersRequest.response])
    return (
        <div className="row">
            <div className="col-sm-9">
                <FormSelect onChange={e => setSelectedUser(e.target.value)}>
                    <option>Select Users</option>
                    {users.map(user =>
                    <option key={user['id']} value={user['username']}>{user['username']}</option>)
                    }
                </FormSelect>
                
            </div>
            <div className="col-sm-3">
                <button className="btn btn-primary">Add User Role</button>
            </div>
        </div>
    )
}
