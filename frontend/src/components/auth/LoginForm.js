import React from 'react'
import Card from "react-bootstrap/Card"
import Container from "react-bootstrap/Container"
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button'
export default function LoginForm() {
  return (
    <Container fluid>

      <Card className='mx-auto w-25 mt-5 shadow-sm' style={{ "width": "20rem" }}>
        <Card.Body>

          <Form.Select aria-label="Default select example">
            <option>Select User to Login</option>
            <option value="1">User #1</option>
            <option value="2">User #2</option>
            <option value="3">User #3</option>
          </Form.Select>

          <div className="d-grid gap-2 mt-3">
            <Button variant="primary">
              login
            </Button>

          </div>

        </Card.Body>
      </Card>

    </Container>
  )
}
