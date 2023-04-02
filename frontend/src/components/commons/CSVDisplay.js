import React from 'react'
import useParser from '../../hooks/useParser'

export default function CSVDisplay({csv}) {
const { columns, rows } = useParser(csv)
  return (
    <div className="container-fluid px-0">
    <div className="row g-0 h-100">
      <div className="col-lg-12 border vh-50">
        <table className="table" >
          <thead>
            <tr>
              <th scope="col">#</th>
              {columns && columns.map((col) => <th scope="col">{col}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows && rows.map((row, index) => (
              <tr>
                <th scope="row">{index}</th>
                {columns.map(col=> <td scope="col">{row[col] ?? '___'}</td>)}
              </tr>
            ))}

          </tbody>
        </table>
      </div>

    </div>
  </div>
  )
}
