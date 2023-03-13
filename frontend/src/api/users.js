import axios from "axios"

export const getAllUsers = async () => {
  const res = await axios.get("./mock-data/users.json")
  return res
}

