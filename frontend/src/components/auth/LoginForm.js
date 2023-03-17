import React, {useState, useEffect} from 'react'
import { useNavigate } from 'react-router-dom';
import Card from "react-bootstrap/Card"
import Container from "react-bootstrap/Container"
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button'
import { getAllUsers } from '../../api/users';
import { useAuth } from '../../context/UserContext';

export default function LoginForm() {
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const {login} = useAuth()
  const navigate = useNavigate()

  const handleLogin = (e) => {
    e.preventDefault()
    login(selectedUser)
    navigate("/")
  }

  useEffect(() => {
    if(sessionStorage.getItem("session") != null) navigate("/")
    getAllUsers().then(res => {
      console.log('users', res)
      setUsers(res.data)
    })
  }, [])
  
  return (
    <Container fluid>

      <Card className='mx-auto w-25 mt-5 shadow-sm' style={{ "width": "20rem" }}>
        <Card.Body>

          <Form onSubmit={handleLogin}>
          <Form.Select aria-label="Default select example" onChange={e => setSelectedUser(e.target.value)}>
          <option>Log in as</option>
            {users.map(user => 
            <option value={JSON.stringify(user)}>{user['username']}</option>)
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
