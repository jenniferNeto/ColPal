import axios from "axios"

export const getAllUsers = async () => {
  const res = await axios.get("http://127.0.0.1:8080/users/")
  console.log("get_all_users", res)
  return res
}

export const getUserPipelines = async (id) => {
  const res = await axios.get(`http://127.0.0.1:8080/pipelines/user/${id}/`)
  console.log("get_user_pipelines", res)
  return res
}
