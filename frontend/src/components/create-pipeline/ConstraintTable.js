import React from 'react'

export default function ConstraintTable({constraints}) {
  return (
    <table className="min-w-full text-left text-sm">
    <thead className='border-b dark:border-neutral-500'>
      <tr>
        <th scope="col" className='p-3'>Constraint Column Name</th>
        <th scope="col" className='p-3'>Constraint Column Type</th>
      </tr>
    </thead>
    <tbody>
      {constraints.map(({column_title, column_name, column_type}) => (
        <tr className="border-b dark:border-neutral-500">
          <td scope="row" className='whitespace-nowrap p-3'>{column_title || column_name}</td>
          <td scope='row' className='whitespace-nowrap p-3'>{column_type}</td>
        </tr>
      ))}
    </tbody>
  </table>
  )
}
