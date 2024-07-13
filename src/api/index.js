import http from '../http'

const API = {
  'searchEmojiByKeyword': '/index',
  'emoteDetail': '/detail'
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

export async function getEmojiDetailById(id) {
  try {
    return await http.get(API.emoteDetail, {
      params: { id }
    })
  } catch (e) {
    throw `网络错误: ${e}`
  }
}