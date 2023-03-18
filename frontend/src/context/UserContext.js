import React, { useContext, useState } from "react"
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
    window.sessionStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    console.log(e)
  }
}

export function UserProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(getSessionStorage('user', null))
  const [accessToken, setAccessToken] = useState(getSessionStorage('access', null))

  const login = async (user) => {

    try {
      let data = new FormData();
      data.append("username", user['username'])
      data.append("password", '.')

      const res = await axios.post("http://127.0.0.1:8000/users/obtain/", data)

      const { access, refresh } = res.data

      setSessionStorage('access', access)
      setSessionStorage('refresh', refresh)
      setSessionStorage('user', user)
      setCurrentUser(user)
      setAccessToken(access)

    } catch (err) {
      console.log(err)
    }

  }

  const logout = () => {
    sessionStorage.clear()
    setCurrentUser(null)
  }


  
  const value = {
    currentUser,
    accessToken,
    login,
    logout,
  }


  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  )
}
