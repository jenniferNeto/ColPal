import React from 'react'
import Card from 'react-bootstrap/Card'
import { Link } from 'react-router-dom'
export default function PipelineCard(props) {
  const {id} = props
  return (
    <Link to={"/pipeline/"+id}>
      <Card style={{border: 'none', background: '#E9E7FD'}}>
          <Card.Body>Pipeline</Card.Body>
      </Card>
    </Link>
  )
}
