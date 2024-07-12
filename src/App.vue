<template>
  <div class="flex flex-col px-[10px] py-4">
    <!-- tab -->
    <div class="tab-list flex gap-2 mb-2 text-sm transition-colors">
      <button class="tab-list-item active">表情包</button>
      <button class="tab-list-item">直播间表情包</button>
      <button class="tab-list-item">充电表情</button>
    </div>
    <!-- search -->
    <div class="search relative shadow-[0_1px_3px_rgba(15,23,42,0.08)]">
      <input :disabled="params.loading" @keyup.enter="search()" class="px-4 py-2 w-full text-xl round-md" type="text"
        v-model="params.keyword" placeholder="输入关键字搜索...">
      <button :disabled="params.loading" class="absolute right-2 top-[8px]" @click="search()">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>
      </button>
    </div>

    <div v-if="!searchResult.list.length" class="flex flex-col items-center justify-center mt-12">
      <img class="w-24 h-24 opacity-60" src="./assets/images/akr-empty.webp" alt="\阿卡林~/">
      <p class="text-slate-400 mt-2">什么都没找到</p>
    </div>

    <!-- results -->
    <section class="emoji-pack my-2 p-4 rounded-md border ring-1 ring-inset ring-slate-50 relative"
      :class="pack.expanded ? 'pb-2' : 'pb-[36px]'" v-for="pack in searchResult.list" :key="pack.id">
      <!-- header -->
      <div class="flex mb-4 pb-1">
        <p class="text-lg text-gray-800 hover:text-blue-400 transition-colors"><a :href="pack.meta.item_url"
            target="_blank">
            {{ pack.text
            }}({{ pack.emote.length }})</a></p>
        <div class="flex-1"></div>
        <button :disabled="pack.downloading" class="download disabled:text-gray-300" @click="download(pack)">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
        </button>
      </div>
      <!-- content -->
      <div class="grid grid-cols-4 gap-2 overflow-hidden py-1 transition-all"
        :class="pack.expanded ? 'h-auto' : 'h-[245px]'">
        <div v-for="e in pack.emote" :key="e.id">
          <div class="emote-image relative flex justify-center py-1 overflow-hidden">
            <img :data-id="e.id" v-lazy class="transition-all w-[120px] h-[120px] object-contain"
              :class="e.dlProgress === 100 ? 'rounded  ring-1 ring-green-500' : (e.dlProgress === '-1' ? 'rounded ring-1 ring-red-500' : '')"
              :data-src="e.url" :alt="e.text">
            <!-- download single -->
            <div @click="downloadSingle(e, true)"
              class="emote-image-bottom transition-all absolute -bottom-[1.25rem] bg-gray-600/50 w-full flex justify-center h-5">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-4 text-white">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
              </svg>
            </div>
          </div>
        </div>
      </div>
      <div @click=" expandCard(pack)" v-if="pack.emote.length > 8 && !pack.expanded"
        class="absolute bottom-0 left-0 cursor-pointer w-full flex justify-center text-slate-300 bg-gradient-to-b from-transparent to-slate-100">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
        </svg>
      </div>
    </section>

  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { vLazy } from './directives/lazy';
import { wrap } from './utils';
import * as API from './api'
import JSzip from 'jszip'
import { saveAs } from 'file-saver'

onMounted(() => {
  // init infinte scrolling
  /// todo: 添加防抖
  document.addEventListener('scroll', (e) => {
    const { scrollTop, scrollHeight } = document.documentElement
    const height = window.innerHeight
    if (scrollTop + height > scrollHeight - 100 && searchResult.value.page.total && !params.value.loading) {
      params.value.pn += 1
      search(false)
    }
  })
})

const params = ref({
  keyword: '',
  pn: 1,
  ps: 5,
  type: '',
  loading: false
})

const searchResult = ref({
  list: [],
  page: {}
})

/**
 * @param reset 是否从第一页开始搜索
 */
const search = wrap(async (reset = true) => {
  const { keyword } = params.value
  if (!keyword) {
    return
  }

  if (reset) {
    params.value.pn = 1
    searchResult.value.list = []
  }

  const resp = await API.searchEmojiByKeyword({
    business: 'reply',
    pn: params.value.pn,
    ps: params.value.ps,
    name: keyword
  })

  if (resp.code !== 0) {
    alert('请求失败')
    return
  }

  const list = (resp.data.list || [])
  searchResult.value.list.push(...list.map((item) => {
    return {
      ...item,
      emote: item.emote.map((e) => {
        return {
          ...e,
          dlProgress: 0,
        }
      }),
      downloading: false,
      expanded: false,
    }
  }))
  searchResult.value.page = resp.data.page
  if (resp.data.page.total < params.value.ps) {
    searchResult.value.page.total = 0
  }
}, () => params.value.loading = true, () => params.value.loading = false)

const download = async (pack) => {
  const generatePackInfoText = () => {
    const urls = pack.emote.map(e => `# ${e.text}\n${e.url}`).join('\n')
    return `# ${pack.text} ${pack.meta.item_url}\n${urls}`
  }

  expandCard(pack)

  pack.downloading = true;

  const zip = new JSzip()
  for (const e of pack.emote) {
    try {
      const { filename, blob } = await downloadSingle(e)
      zip.file(filename, blob)
    } catch (e) {
      e.dlProgress = -1
      console.error(e)
    }
  }

  zip.file('info.txt', generatePackInfoText())

  zip.generateAsync({ type: "blob" }).then(data => {
    saveAs(data, pack.text + '.zip')
  })

  pack.downloading = false;
}

const downloadSingle = async (e, save = false) => {
  const resp = await fetch(e.url.replace('http:', location.protocol))
  const filename = e.text + e.url.slice(e.url.lastIndexOf('.'))
  const blob = await resp.blob()

  e.dlProgress = 100;

  if (save) {
    saveAs(blob, filename)
  } else {
    return { blob, filename }
  }
}

const expandCard = (pack) => {
  pack.expanded = true
}

</script>

<style lang="scss" scoped>
.tab-list-item {
  @apply text-slate-700 inline-block py-2 px-4 rounded-3xl text-sm;
}

.tab-list-item.active {
  @apply text-slate-900 bg-slate-100;
}

.emote-image:hover>.emote-image-bottom {
  cursor: pointer;
  bottom: 0;
}
</style>