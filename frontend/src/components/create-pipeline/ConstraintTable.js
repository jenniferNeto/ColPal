import React from 'react'

export default function ConstraintTable({constraints}) {
  return (
    <table>
    <thead>
      <tr>
        <th>Column Name</th>
        <th scope="col">Column Type</th>
      </tr>
    </thead>
    <tbody>
      {constraints.map(({column_title, column_name, column_type}) => (
        <tr>
          <th scope="row">{column_title || column_name}</th>
          <td>{column_type}</td>
        </tr>
      ))}
    </tbody>
  </table>
  )
}
