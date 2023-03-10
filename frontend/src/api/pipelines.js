import axios from "axios"

export const getAllPipelines = async () => {
  const res = await axios.get("./mock-data/pipelines.json")
  return res
}

