import React from 'react'
import Card from 'react-bootstrap/Card'
import { Link } from 'react-router-dom'
export default function PipelineCard({data}) {
  const {id, title} = data
  return (
    <Link to={"/pipeline/"+id}>
      <Card style={{border: 'none', background: '#E9E7FD'}}>
          <Card.Body>{title}</Card.Body>
      </Card>
    </Link>
  )
}
