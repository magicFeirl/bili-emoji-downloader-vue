import http from '../http'

const API = {
  'searchEmojiByKeyword': '/index'
}

export async function searchEmojiByKeyword(params) {
  return await http.get(API.searchEmojiByKeyword, {
    params
  })
}