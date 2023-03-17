import axios from "axios"

export const getAllUsers = async () => {
  const res = await axios.get("http://127.0.0.1:8000/users/")
  console.log("get_all_users", res)
  return res
}

export const getAllUserPipelines = async (id) => {
  const res = await axios.get(`http://127.0.0.1:8000/pipelines/user/${id}`, { withCredentials: true })
  console.log("get_all_user_pipelines", res)
  return res
}


