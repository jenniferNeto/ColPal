import React from 'react'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHouse, faPlus, faCheck } from "@fortawesome/free-solid-svg-icons";
import logo from '../../img/logo-white.png'

export default function Sidebar() {
  return (
    
            <div class="d-flex flex-sm-column flex-row flex-nowrap bg-light align-items-center sticky-top bg-black text-white">
                <a href="/" class="d-block px-1 py-3 text-decoration-none" title="" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-original-title="Icon-only">
                    <img src={logo} alt='logo' className="rounded" style={{'width': '75px'}}/>
                </a>
                <hr/>
                <ul class="nav nav-pills nav-flush flex-sm-column flex-row flex-nowrap mb-auto mx-auto text-center justify-content-between w-100 px-3 align-items-center">

                    <li class="nav-item">
                        <a href="/" class="nav-link px-1 py-3 text-white" title="" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-original-title="Home">
                            <FontAwesomeIcon icon={faHouse} inverse size="2x"/>
                            
                            <span className='d-block mt-2'>Home</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="/" class="nav-link px-1 py-3 text-white" title="" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-original-title="Home">
                            <FontAwesomeIcon icon={faPlus} inverse size="2x"/>
                            <span className='d-block mt-2'>Create</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="/" class="nav-link px-1 py-3 text-white" title="" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-original-title="Home">
                            <FontAwesomeIcon icon={faCheck} inverse size="2x"/>
                            <span className='d-block mt-2'>Approve</span>
                        </a>
                    </li>
                  
                    
                </ul>
              
          
            </div>
        
  )
}
