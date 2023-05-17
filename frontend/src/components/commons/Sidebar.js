import React, { useState } from 'react'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHouse, faPlus, faCheck, faSignOut } from "@fortawesome/free-solid-svg-icons";
import logo from '../../img/logo-white.png'
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/UserContext';
export default function Sidebar() {
    const {logout, currentUser} = useAuth()
    return (

        <div className="bg-main-500 d-flex flex-sm-column flex-row flex-nowrap align-items-center sticky-top rounded h-100 shadow px-1">
            <a href="/" className="d-block px-1 py-3 text-decoration-none">
                <img src={logo} alt='logo' className="rounded" style={{ 'width': '75px' }} />
            </a>
            <hr className="hr" />
            <ul className="nav nav-pills nav-flush flex-sm-column flex-row flex-nowrap mb-auto mx-auto text-center justify-content-between w-100 px-3 align-items-center">

                <li className="nav-item">
                    <Link to="/" className="nav-link px-1 py-3 text-white" title="">
                        <FontAwesomeIcon icon={faHouse} size="2x" />
                        <span className='d-block mt-2'>Home</span>
                    </Link>
                </li>
                <li className="nav-item">
                    <Link to="/pipeline-create" className="nav-link px-1 py-3 text-white" title="">
                        <FontAwesomeIcon icon={faPlus} size="2x" />
                        <span className='d-block mt-2'>Create</span>
                    </Link>
                </li>
                {currentUser.admin && (
                    <li className="nav-item">
                    <Link to="/pipeline-verify" className="nav-link px-1 py-3 text-white" title="">
                        <FontAwesomeIcon icon={faCheck} size="2x" />
                        <span className='d-block mt-2'>Approve</span>
                    </Link>
                </li>
                )}
                
                <li className="nav-item">
                    <Link onClick={logout} className="nav-link px-1 py-3 text-white" title="">
                        <FontAwesomeIcon icon={faSignOut} size="2x" />
                        <span className='d-block mt-2'>Logout</span>
                    </Link>
                </li>


            </ul>


        </div>

    )
}
