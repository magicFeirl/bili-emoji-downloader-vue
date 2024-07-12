import http from '../http'

const API = {
  'searchEmojiByKeyword': '/search'
}

export async function searchEmojiByKeyword(params) {
  return await http.get(API.searchEmojiByKeyword, {
    params
  })
}