import http from '../http'

const API = {
  'searchEmojiByKeyword': '/index',
  'emoteDetail': '/detail'
}

export async function searchEmojiByKeyword(params) {
  return await http.get(API.searchEmojiByKeyword, {
    params
  })
}

export async function getEmojiDetailById(id) {
  return await http.get(API.emoteDetail, {
    params: { id }
  })
}