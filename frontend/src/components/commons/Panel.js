import React from 'react'

export default function Panel({children}) {
  return (
    <div className='bg-white shadow h-full my-2 p-3 rounded'>
        {children}
    </div>
  )
}
