<template>
  <div class="flex flex-col px-[10px] py-4">
    <!-- config dialog -->
    <div
      v-if="configDialog.show"
      @click="closeConfigDialog"
      class="px-2 z-50 left-0 right-0 top-0 bottom-0 fixed bg-black/30 flex justify-center items-center"
    >
      <!-- config dialog body -->
      <div @click.stop class="sm:w-1/2 w-full bg-white rounded p-4">
        <div class="form-item">
          <label for="cookie">配置本地 Cookie</label>
          <p class="text-slate-400 text-sm mb-4">
            如果遇到"账号未登录"问题，请在此处配置自己的B站Cookie，配置成功后将使用配置的Cookie进行请求。网站后端不会存储任何数据，源码右上角可见。
          </p>
          <textarea
            placeholder="SESSDATA=xxx;bili_jct=xxx;...."
            v-model="configDialog.cookie"
            name="cookie"
            id="cookie"
            cols="30"
            rows="10"
          ></textarea>
        </div>

        <div class="mt-4 text-right">
          <button
            @click="closeConfigDialog"
            class="px-2 py-1 rounded bg-red-400 mr-1 text-white"
          >
            取消
          </button>
          <button
            @click="saveConfig"
            class="px-2 py-1 rounded bg-blue-400 text-white"
          >
            确定
          </button>
        </div>
      </div>
    </div>
    <!-- tab -->
    <div class="tab-list flex gap-2 mb-3 text-sm transition-colors">
      <button
        v-for="tab in tabBar.list"
        :key="tab.id"
        @click="switchTab(tab)"
        class="tab-list-item"
        :class="{ active: tab.id === tabBar.currentTabId }"
      >
        {{ tab.name }}
      </button>
      <!-- <button @click="showChargeEmoteHelper" class="tab-list-item">充电表情</button> -->
      <div class="flex-1"></div>

      <a title="配置cookie" href="/#" @click.prevent="openConfigDialog">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-6 text-slate-600"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
          />
        </svg>
      </a>

      <a
        title="部署同款网站"
        target="_blank"
        href="https://github.com/magicFeirl/bili-emoji-downloader-vue"
      >
        <svg
          viewBox="0 0 24 24"
          aria-hidden="true"
          class="size-6 fill-slate-600"
        >
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M12 2C6.477 2 2 6.463 2 11.97c0 4.404 2.865 8.14 6.839 9.458.5.092.682-.216.682-.48 0-.236-.008-.864-.013-1.695-2.782.602-3.369-1.337-3.369-1.337-.454-1.151-1.11-1.458-1.11-1.458-.908-.618.069-.606.069-.606 1.003.07 1.531 1.027 1.531 1.027.892 1.524 2.341 1.084 2.91.828.092-.643.35-1.083.636-1.332-2.22-.251-4.555-1.107-4.555-4.927 0-1.088.39-1.979 1.029-2.675-.103-.252-.446-1.266.098-2.638 0 0 .84-.268 2.75 1.022A9.607 9.607 0 0 1 12 6.82c.85.004 1.705.114 2.504.336 1.909-1.29 2.747-1.022 2.747-1.022.546 1.372.202 2.386.1 2.638.64.696 1.028 1.587 1.028 2.675 0 3.83-2.339 4.673-4.566 4.92.359.307.678.915.678 1.846 0 1.332-.012 2.407-.012 2.734 0 .267.18.577.688.48 3.97-1.32 6.833-5.054 6.833-9.458C22 6.463 17.522 2 12 2Z"
          ></path>
        </svg>
      </a>
    </div>
    <!-- search -->
    <div class="search relative card-shadow mb-2">
      <input
        :disabled="loadingState == 'loading'"
        @keyup.enter="search()"
        class="text-slate-600 px-4 py-2 w-full rounded-md"
        type="text"
        v-model="params.keyword"
        :placeholder="activeTab.placeholder"
      />
      <button
        :disabled="loadingState == 'loading' || !params.keyword"
        class="absolute right-2 top-[8px] disabled:text-gray-300"
        @click="search()"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
          />
        </svg>
      </button>
    </div>

    <div
      v-if="isNoData && loadingState == 'null'"
      class="flex flex-col items-center justify-center mt-12"
    >
      <img
        class="w-24 h-24 opacity-60"
        src="./assets/images/akr-empty.webp"
        alt="\阿卡林~/"
      />
      <p class="text-slate-400 mt-2">什么都没找到</p>
    </div>

    <template v-if="activeTab.type === 'emote'">
      <ImageGrid
        v-for="result in searchResult.list"
        :key="result.pack.id"
        :pack="result.pack"
        :item_url="result.item_url"
        :title="result.title"
        :imageList="result.imageList"
        :type="{ apiType: params.apiType, emoteType: 'emote' }"
        @search-suit="handleSearchSuit"
      ></ImageGrid>
    </template>
    <template v-else-if="activeTab.type === 'collection'">
      <CollectionGrid>
        <CollectionItem
          @search-emoji="handleSearchEmoji"
          v-for="item in colSearchResult.list"
          :key="item.id"
          :data="item"
        ></CollectionItem>
      </CollectionGrid>
    </template>

    <div
      v-if="loadingState == 'loading'"
      class="text-slate-400 text-center mt-16"
    >
      搜索中...
    </div>
    <div
      v-else-if="loadingState == 'error'"
      class="text-lg text-red-600/60 text-center my-8"
    >
      加载失败: {{ searchResult.errorMsg || "未知错误" }}
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, nextTick } from "vue";
import { wrap } from "@/utils";
import * as API from "@/api";

import ImageGrid from "@/components/ImageGrid/ImageGrid.vue";
import CollectionGrid from "@/components/Collection/CollectionGrid.vue";
import CollectionItem from "@/components/Collection/CollectionItem.vue";

onMounted(() => {
  // init infinte scrolling
  /// todo: 添加防抖
  document.addEventListener("scroll", async (e) => {
    const { scrollTop, scrollHeight } = document.documentElement;
    const height = window.innerHeight;

    if (scrollTop + height > scrollHeight - 100) {
      await loadNext();
    }
  });
});

const loadNext = async () => {
  const { total, ps, pn } =
    activeTab.value.type === "collection"
      ? colSearchResult.value.page
      : searchResult.value.page;
  const hasNext = pn * ps < total;

  // console.log(hasNext, pn, ps, total, loadingState.value);

  if (hasNext && loadingState.value == "null") {
    params.value.pn += 1;
    await search(false);
  }
};

const tabBar = ref({
  currentTabId: 0,
  list: [
    { id: 0, name: "表情包", placeholder: "输入关键字搜索", type: "emote" },
    {
      id: 1,
      name: "装扮/收藏集",
      placeholder: "输入关键字搜索",
      type: "collection",
    },
    {
      id: 2,
      name: "直播间表情包",
      placeholder: "输入直播间 ID 或 URL",
      type: "emote",
    },
  ],
});

const activeTab = computed(() =>
  tabBar.value.list.find((b) => b.id === tabBar.value.currentTabId)
);

const isNoData = computed(() => {
  return !searchResult.value.list.length && !colSearchResult.value.list.length;
});

const params = ref({
  keyword: "",
  pn: 1,
  ps: 5,
  // app | pc
  apiType: "app",
  cookie: localStorage.getItem("bili-emoji-downloader-cookie"),
});

const configDialog = ref({
  show: false,
  cookie: "",
});

const closeConfigDialog = () => {
  configDialog.value.cookie = "";
  configDialog.value.show = false;
};

const openConfigDialog = () => {
  configDialog.value.cookie = params.value.cookie;
  configDialog.value.show = true;
};

const saveConfig = () => {
  const cookie = configDialog.value.cookie.trim();

  const isValidCookie = (cookie) => {
    const keys = cookie
      .split(";")
      .map((c) => c.split("="))
      .filter((c) => c.length)
      .map((c) => c[0].trim().toLowerCase());
    return keys.includes("bili_jct") && keys.includes("sessdata");
  };

  if (cookie && !isValidCookie(cookie)) {
    alert("无效的Cookie：Cookie 必须包含 sessdata 和 bili_jct 字段");
    return;
  }

  localStorage.setItem("bili-emoji-downloader-cookie", cookie);
  params.value.cookie = cookie;

  closeConfigDialog();
};

const loadingState = ref("null"); // null | loading | error

const searchResult = ref({
  list: [
    /*{ imageList: [], title: "", meta: {} }*/
  ],
  errorMsg: "",
  method: "",
});

const colSearchResult = ref({
  list: [],
  page: {},
  errorMsg: "",
});

const switchTab = async (tab) => {
  tabBar.value.currentTabId = tab.id;
  // 清空搜索结果
  searchResult.value.list = [];
  colSearchResult.value.list = [];

  if (params.value.keyword) {
    await search();
    // const { id } = activeTab.value;
    //id=0: 自动搜索表情包; 1自动搜索收藏集
    // if (id === 0) {
    //   await searchEmoji();
    // } else if (id === 1) {
    //   await searchCollection();
    // }
  }
  // params.value.keyword = "";
};

const handleSearchFromTab = (kw, tabIdx) => {
  params.value.keyword = kw;
  switchTab(tabBar.value.list[tabIdx]);
};

const handleSearchEmoji = (kw) => {
  handleSearchFromTab(kw, 0);
};

const handleSearchSuit = (kw) => {
  handleSearchFromTab(kw, 1);
};

const formatApiResult = (apiType, resp) => {
  const list =
    apiType === "app" ? resp.data.list || [] : resp.data.packages || [];
  const emoteK = apiType === "app" ? "emote" : "emotes";

  return list.map((item) => {
    const maxLen = params.value.apiType === "app" ? 12 : 8;

    return {
      ...item,
      emote: item[emoteK].map((e) => {
        return {
          ...e,
          dlProgress: 0,
        };
      }),
      downloading: false,
      tojpg: true,
      expanded:
        item[emoteK].length <= maxLen ||
        (params.value.apiType === "pc" && window.innerWidth < 540),
    };
  });
};

const jumpToLiveEmoteAPI = (keyword) => {
  const room_id =
    keyword.match(/live\.bilibili\.com\/(\d+).+?/) || keyword.match(/^(\d+)$/);
  if (!room_id || !room_id[1]) {
    alert("无法查找房间 ID: " + keyword);
    return;
  }

  const url =
    "https://api.live.bilibili.com/xlive/web-ucenter/v2/emoticon/GetEmoticons?platform=pc&room_id=" +
    room_id[1];
  open(url, "_blank");
};

const searchEmoji = async () => {
  // 直播间表情包跳转到表情包接口
  if (activeTab.value.id === 1) {
    return jumpToLiveEmoteAPI(keyword);
  }

  const resp = await API.searchEmojiByKeyword(
    {
      pn: params.value.pn,
      ps: params.value.ps,
      name: params.value.keyword,
    },
    {
      "x-bili-cookie": params.value.cookie,
    }
  );

  if (resp.code !== 0) {
    throw `code:${resp.code} message:${resp.message}`;
  }

  // 考虑到配置难度后端也提供了用 cookie 请求的接口，两种接口格式不同但是对用户来说是无感的，所以前端需要统一一下，将接口格式都转为 app 端的格式
  const apiType = (params.value.apiType =
    resp.data.MobiApp != undefined ? "app" : "pc");

  for (const item of formatApiResult(apiType, resp)) {
    searchResult.value.list.push({
      imageList: [...item.emote],
      title: item.text,
      item_url: item.meta.item_url,
      pack: { ...item },
    });
  }

  // pc 端分页转为移动端分页格式
  if (apiType === "pc") {
    const { total, ps, pn } = resp.data;
    resp.data.page = {
      total,
      ps,
      pn,
    };
  }

  searchResult.value.page = resp.data.page;
};

const searchCollection = async () => {
  const resp = await API.getCollectionList({
    keyword: params.value.keyword,
    pn: params.value.pn,
    ps: 20,
  });

  if (resp.code !== 0) {
    throw `code:${resp.code} message:${resp.message}`;
  }

  colSearchResult.value.list.push(...resp.data.list);
  const { pn, ps, total } = resp.data;
  colSearchResult.value.page = { pn, ps, total };
};

/**
 * @param reset 是否从第一页开始搜索
 */
const search = wrap(
  async (reset = true) => {
    const { keyword } = params.value;
    if (!keyword) {
      return;
    }

    if (reset) {
      params.value.pn = 1;
      searchResult.value.list = [];
      colSearchResult.value.list = [];
    }

    if (activeTab.value.type === "emote") {
      await searchEmoji();
    } else if (activeTab.value.type === "collection") {
      await searchCollection();
    }
  },
  () => (loadingState.value = "loading"),
  (state, error) => {
    loadingState.value = "null";

    if (state == "error") {
      loadingState.value = "error";
      searchResult.value.errorMsg = error;
    }
   
    // 没有滚动条，自动加载下一页
    nextTick(() => {
      if (document.body.scrollHeight <= window.innerHeight) {
        loadNext().then(() => {});
      }
    });
  }
);

// const url = new URL(location.href)
// const kw = url.searchParams.get('kw')
// if (kw) {
//   params.keyword = kw
//   search()
// }
</script>

<style lang="scss" scoped>
.tab-list-item {
  @apply text-slate-700 inline-block py-2 px-4 rounded-3xl text-sm;
}

.tab-list-item.active {
  @apply text-slate-900 bg-slate-100;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.15);
}

.card-shadow {
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.15);
}

.form-item {
  @apply flex flex-col;
}

.form-item label {
  @apply text-slate-600 text-lg mb-2 font-bold;
}

.form-item textarea,
.form-item input {
  @apply ring-1 ring-slate-300 rounded-lg p-2;
}
</style>
