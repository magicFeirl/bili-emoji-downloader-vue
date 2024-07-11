import axios from "axios"

const inst = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 1000 * 5
})

inst.interceptors.response.use((config) => {
  return config.data
})

export default inst