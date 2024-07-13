import axios from "axios"

const inst = axios.create({
  baseURL: '/api',
  timeout: 1000 * 5
})

inst.interceptors.request.use((config) => {
  return config
}, (error) => {
  throw `请求失败: ${error}`
})

inst.interceptors.response.use((config) => {
  return config.data
})



export default inst