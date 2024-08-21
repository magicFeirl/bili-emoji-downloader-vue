
const obs = new IntersectionObserver((items) => {
  for (const item of items) {
    if (item.isIntersecting) {
      const { target } = item
      const src = target.getAttribute('data-src')
      if (src) {
        target.src = src
      }
      obs.unobserve(item.target)
    }
  }
}, {
  rootMargin: '0px 0px 100px 0px'
})

export const vLazy = {
  beforeMount: (el, bindings) => {
    // bg修饰添加背景
    if (bindings.modifiers.bg) {
      el.style.backgroundColor = `rgb(148 163 184 / 0.4)`
    }
    obs.observe(el)
  },
  beforeUnmount(el) {
    obs.unobserve(el)
  }
}
