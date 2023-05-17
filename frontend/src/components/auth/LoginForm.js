import React, { useState, useEffect } from 'react'
import logo from '../../img/logo-white.png'
import { useNavigate } from 'react-router-dom';
import Card from "react-bootstrap/Card"
import Container from "react-bootstrap/Container"
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button'
import { get_all_users } from '../../utils/endpoints';
import { useAuth } from '../../context/UserContext';
import useRequest from '../../hooks/useRequest';

export default function LoginForm() {
  const [selectedUser, setSelectedUser] = useState(null)
  const { currentUser, login } = useAuth()
  const {response: users, doRequest: allUsersRequest} = useRequest(get_all_users())
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()

    if (selectedUser == null) return;

    const userData = users.data.find(user => user['username'] == selectedUser)
    
    await login(userData)

    navigate("/")

  }

  useEffect(() => {
    if (currentUser != null) navigate("/")

    allUsersRequest()
  }, [allUsersRequest])

  return (
    <Container fluid>

      <Card className='mx-auto text-center w-25 mt-5 shadow-sm' style={{ "width": "20rem" }}>
  
      
        <Card.Body>
        <img src={logo} alt='logo' className="card-img-top mx-auto rounded ms-auto" style={{ 'width': '150px' }} />
          <Form onSubmit={handleLogin}>
            <Form.Select aria-label="Default select example" onChange={e => setSelectedUser(e.target.value)}>
              <option>Log in as</option>
              {users && users.data.map(user =>
                <option key={user['id']} value={user['username']}>{user['username']}</option>)
              }

            </Form.Select>

            <div className="d-grid gap-2 mt-3">
              <Button type="submit" variant="primary">
                Login
              </Button>

            </div>
          </Form>
        </Card.Body>

      </Card>

    </Container>
  )
}
