// 包裹 Promise
export function wrap(p, before, after) {
  return (...args) => {
    before()

    return p(...args).finally(() => {
      after()
    })
  }
}