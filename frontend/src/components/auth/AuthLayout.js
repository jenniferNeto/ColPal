import React from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { useAuth } from '../../context/UserContext'
import Sidebar from "../commons/Sidebar"

export default function AuthLayout() {
  const {currentUser} = useAuth()
 
  return (
    
      currentUser !== null ? (
        <div class="container-fluid">
        <div class="row">
            <div class="col-sm-auto sticky-top py-2">
                <Sidebar />
            </div>
            <div class="container col-sm p-2 min-vh-100">
                <Outlet />
            </div>
        </div>
    </div>
      ) : (
        <Navigate to={"/login"} replace />
      )
    
    
  )
}
