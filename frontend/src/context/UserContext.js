import React, { useContext, useEffect, useState } from "react"
import axios from "axios"

const UserContext = React.createContext()

export function useAuth() {
  return useContext(UserContext)
}

const getSessionStorage = (key, initialValue) => {
    try {
      const value = window.sessionStorage.getItem(key);
      return value ? JSON.parse(value) : initialValue;
    } catch (e) {
      // if error, return initial value
      return initialValue;
    }
}

function setSessionStorage(key, value) {

    try {
      window.sessionStorage.setItem(key, value);
    } catch (e) {
      console.log(e)
    }
  }

export function UserProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(getSessionStorage('user', null))

  const login = async (user) => {
    
    setSessionStorage('user', user)

    setCurrentUser(getSessionStorage('user', null))

  }

  const logout = () => {
    sessionStorage.clear()
    setCurrentUser(null)
  }
  
  const value = {
    currentUser,
    login,
    logout
  }

  useEffect(() => {
    const get_jwt = async () => {
      if(currentUser == null) return
      let data = new FormData();
      data.append("user", currentUser['username'])
      
      await axios.post("http://127.0.0.1:8000/users/obtain/")
      console.log("login_jwt", res)
  
    }

    get_jwt()

  }, [currentUser])



  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  )
}
