import http from '../http'

const API = {
  'searchEmojiByKeyword': '/index'
}

export async function searchEmojiByKeyword(params) {
  try {
    return await http.get(API.searchEmojiByKeyword, {
      params
    })
  } catch (e) {
    throw `网络错误: ${e}`
  }
}