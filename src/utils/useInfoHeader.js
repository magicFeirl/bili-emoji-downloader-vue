export default function useInfoHeader({
  title = "",
  name,
  jumplink,
  urls
}) {
  title = title || `由 ${location.href} 导出，项目地址: https://github.com/magicFeirl/bili-emoji-downloader-vue\n# 表情包版权归原作者所有`;

  if (Array.isArray(urls)) {
    urls = urls.map(({ name, url }) => `# ${name}\n${url}\n`).join('\n')
  }

  return `
    # ${title}
    # 名称：${name}
    # 购买地址: ${jumplink}
    -*
    ${urls}
  `.replace(/^\s+/gm, '').replace(/(-\*)/g, '\n')
}