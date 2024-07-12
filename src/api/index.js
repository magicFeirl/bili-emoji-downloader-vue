import http from '../http'

const API = {
  'searchEmojiByKeyword': '/'
}

export async function searchEmojiByKeyword(params) {
  return await http.get(API.searchEmojiByKeyword, {
    params
  })
}