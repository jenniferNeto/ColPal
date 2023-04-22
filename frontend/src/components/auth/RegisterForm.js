import React from 'react'
import Card from "react-bootstrap/Card"
import Container from "react-bootstrap/Container"
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button'
import useRequest from '../../hooks/useRequest';
import { create_user } from '../../utils/endpoints';

export default function RegisterForm() {

  const registerRequest = useRequest(create_user())

  const handleRegister = async (e) => {
    e.preventDefault()
    registerRequest.doRequest({ 'username': e.target.username.value, 'email': e.target.email.value })
  }


  return (
    <Container fluid>

      <Card className='mx-auto w-25 mt-5 shadow-sm' style={{ "width": "20rem" }}>
        <Card.Body>

          <Form onSubmit={handleRegister}>
            
            <input type="text" className='form-control my-1' name="username" placeholder="Username" />
            <input type="text" className='form-control my-1' name="email" placeholder="Email" />
        
            <Button type="submit" variant="primary">Register</Button>

           
           
          </Form>
        </Card.Body>

      </Card>

    </Container>
  )
}
