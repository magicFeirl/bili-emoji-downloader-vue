// 包裹 Promise
export function wrap(p, before, after) {
  return (...args) => {
    before()

    let fin = true
    return p(...args).then(() => {
      fin = false
      after('then')
    }).catch((e) => {
      fin = false
      after('error', e)
      throw e
    }).finally(() => {
      fin && after('finally')
    })
  }
}