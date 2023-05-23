import React from 'react'

export default function Pill({color, text}) {
  return (
    <span class={`bg-${color} inline-block rounded-full px-2 py-1 mx-1 text-sm font-semibold text-white`}>{text}</span>
  )
}
