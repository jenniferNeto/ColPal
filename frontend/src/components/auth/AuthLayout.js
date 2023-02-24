import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from "../commons/Sidebar"

export default function AuthLayout() {

  return (
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-auto bg-light sticky-top bg-black shadow-sm">
                <Sidebar />
            </div>
            <div class="col-sm p-3 min-vh-100">
                <Outlet />
            </div>
        </div>
    </div>
  )
}
