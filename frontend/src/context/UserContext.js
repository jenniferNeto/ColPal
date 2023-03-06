import React, { useContext, useState } from "react"

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
  const [currentUser, setCurrentUser] = useState(getSessionStorage('session', null))

  const login = (session) => {

    setSessionStorage('session', session)
    setCurrentUser(getSessionStorage('session', null))
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


  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  )
}
