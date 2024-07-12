import axios from "axios"

const inst = axios.create({
  baseURL: '/api',
  timeout: 1000 * 5
})

inst.interceptors.response.use((config) => {
  return config.data
})

export default inst