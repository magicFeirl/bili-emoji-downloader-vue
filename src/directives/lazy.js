
const obs = new IntersectionObserver((items) => {
  for (const item of items) {
    if (item.isIntersecting) {
      const { target } = item
      target.src = target.getAttribute('data-src')
      obs.unobserve(item.target)
    }
  }
}, {
  rootMargin: '0px 0px 100px 0px'
})

export const vLazy = {
  beforeMount: (el) => {
    obs.observe(el)
  },
  beforeUnmount(el) {
    obs.unobserve(el)
  }
}
