import http from '../http'

const API = {
  'searchEmojiByKeyword': '/index',
  'emoteDetail': '/detail',
  'collectionList': '/collection',
  'collectionDetail': '/collection-detail',
  'suitDetail': '/suit-detail'
}

export async function searchEmojiByKeyword(params, headers = {}) {
  return await http.get(API.searchEmojiByKeyword, {
    params,
    headers
  })
}

export async function getEmojiDetailById(id) {
  return await http.get(API.emoteDetail, {
    params: { id }
  })
}


export async function getCollectionList(params) {
  return await http.get(API.collectionList, {
    params
  })
}

export async function getCollectionDetail(act_id, lottery_id) {
  return await http.get(API.collectionDetail, {
    params: {
      act_id,
      lottery_id
    }
  })
}

export async function getSuitDetail(item_id) {
  return await http.get(API.suitDetail, {
    params: { item_id }
  })
}