<template>
  <div
    @click="close"
    class="fixed left-0 top-0 right-0 bottom-0 w-full h-full bg-[rgba(31,31,31)]/80 overflow-auto"
  >
    <div @click.stop class="max-w-[720px] mx-auto">
      <header class="relative bg-slate-400/40">
        <div
          class="text-white absolute bottom-0 py-2 px-4 left-0 flex items-center justify-between w-full bg-slate-600/40"
        >
          <h1 class="text-2xl font-bold">
            <a :href="state.jumplink" target="_blank">{{ state.title }}</a>
          </h1>
          <div class="flex-1"></div>

          <button
            title="下载"
            :disabled="state.downloading"
            class="disabled:text-gray-300 mr-4"
            @click="download"
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
                d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"
              />
            </svg>
          </button>

          <!-- selection -->
          <button
            title="选择模式"
            @click="toggleSelectionMode"
            class="flex items-center pt-1"
            :class="{ 'text-green-400': state.selectionMode }"
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
                d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
              />
            </svg>

            <span v-show="selectImages.length" class="ml-2"
              >({{ selectImages.length }} / {{ totalImages }})</span
            >
          </button>

          <button @click="searchEmoji" title="跳转搜索表情包" class="ml-4 mt-1">
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
                d="M15.182 15.182a4.5 4.5 0 0 1-6.364 0M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Z"
              />
            </svg>
          </button>
        </div>

        <!-- close -->
        <button class="absolute right-4 top-2 text-white" @click="close">
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
              d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
            />
          </svg>
        </button>

        <img
          v-lazy.bg
          class="object-cover h-[220px] w-full"
          :class="state.itemType == 'ip' ? 'object-center' : 'object-top'"
          :src="`${state.headerImage}${IMAGE_BUCKET.header}`"
          alt=""
        />
      </header>

      <main class="my-2 mb-8 sm:px-0 px-2">
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div
            @click.stop
            v-for="(item, idx) in state.images"
            class="image-grid-item justify-self-center w-full"
            :class="{ select: item.select }"
            :key="item.id"
          >
            <span v-if="item.filetype === 'video'" class="video-pointer">
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
                  d="m15.75 10.5 4.72-4.72a.75.75 0 0 1 1.28.53v11.38a.75.75 0 0 1-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25h-9A2.25 2.25 0 0 0 2.25 7.5v9a2.25 2.25 0 0 0 2.25 2.25Z"
                />
              </svg>
            </span>

            <span class="select-pointer"></span>
            <img
              v-lazy.bg
              class="rounded-md h-[255px] object-cover w-full"
              :class="{ 'ring ring-green-400': item.downloaded }"
              :data-src="`${item.cover_url.replace(/@.+/, '')}${
                IMAGE_BUCKET.cover
              }`"
              :data-index="idx"
              @click="toggleImageSelect(item)"
            />
          </div>
        </div>
      </main>
    </div>

    <ImagePreview
      @click.stop
      v-model="imagePreview.show"
      :src="imagePreview.src"
    ></ImagePreview>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from "vue";
import * as API from "@/api";
import { vLazy } from "@/directives/lazy";

import ImagePreview from "@/components/Collection/ImagePreview.vue";

import useJSZip from "@/utils/useJSZip.js";
import useInfoHeader from "@/utils/useInfoHeader.js";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const IMAGE_BUCKET = {
  header: ``,
  cover: `@600w_1080h`, //`@1080w_1618h`
};

const data = ref({ ...props.data });

// ip:装扮 | dlc_act: 收藏
const itemType = computed(() => data.value.properties.type);
const state = ref({
  headerImage: "",
  images: [],
  title: "",
  jumplink: "",
  downloading: false,
  selectionMode: false,
});

const imagePreview = ref({
  show: false,
  src: "",
});

const selectImages = computed(() => state.value.images.filter((i) => i.select));
const totalImages = computed(() => state.value.images.length);

const loadCollection = async () => {
  const { dlc_act_id, dlc_lottery_id } = data.value.properties;
  const result = (await API.getCollectionDetail(dlc_act_id, dlc_lottery_id))
    .data;

  state.value.jumplink = `https://www.bilibili.com/h5/mall/digital-card/home?act_id=${dlc_act_id}&lottery_id=${dlc_lottery_id}`;
  state.value.title = result.goods_name;
  state.value.headerImage = `${data.value.properties.image_cover}${IMAGE_BUCKET.header}`;

  state.value.images = result.item_list.map((item) => {
    const info = item.card_info.card_type_info;
    const bg = info.space_background;
    const has_ani = bg.animation;
    let cover_url = has_ani
      ? bg.animation.animation_backup_image
      : info.space_background.image.default_image;

    cover_url = cover_url || info.overview_image;

    let image_url = has_ani ? bg.animation.animation_url : cover_url;
    // 目测较早出的收藏集有的没有 animation_url 字段，用 video_urls 替代
    // animation_video_urls https 协议可以直接播放/下载

    if (has_ani && bg.animation.animation_video_urls) {
      image_url = bg.animation.animation_video_urls[0];
    }

    const ext = image_url.slice(image_url.lastIndexOf("."));

    return {
      cover_url,
      filename: `${info.name}${ext}`,
      filetype: has_ani ? "video" : "image",
      material_type: info.material_type,
      id: cover_url,
      url: image_url,
      select: false,
      downloaded: false,
    };
  });
};

const loadSuit = async () => {
  const { item_id } = data.value;
  const result = (await API.getSuitDetail(item_id)).data;
  state.value.headerImage = `${result.properties.fan_share_image}`;
  state.value.jumplink = `https://www.bilibili.com/h5/mall/suit/detail?navhide=1&id=${result.item_id}`;
  state.value.title = result.name;

  // 把背景图片结构转为 {url, filename, id} 的 Array
  state.value.images = result.suit_items.space_bg
    .map((item) => item.properties)
    .flat()
    .map((item) => {
      return Object.keys(item)
        .filter((key) => key.endsWith("_portrait"))
        .map((key, idx) => {
          const url = item[key];
          const ext = url.slice(url.lastIndexOf("."));
          return {
            cover_url: url,
            url: url,
            filename: `${state.value.title}_${idx}${ext}`,
            id: url,
            select: false,
            downloaded: false,
          };
        });
    })
    .flat();
};

const toggleImageSelect = (item) => {
  if (state.value.selectionMode) {
    return (item.select = !item.select);
  }

  imagePreview.value.show = true;
  imagePreview.value.src = item.cover_url;
};

const toggleSelectionMode = () => {
  state.value.selectionMode = !state.value.selectionMode;
};

const download = async () => {
  const generatePackInfoText = () => {
    console.log(state.value);
    const images = selectImages.value.length
      ? selectImages.value
      : state.value.images;

    return useInfoHeader({
      name: state.value.title,
      jumplink: state.value.jumplink,
      urls: images.map((e) => ({ name: e.filename, url: e.url })),
    });
  };

  state.value.downloading = true;
  const zip = new useJSZip();
  const imageEls = document.querySelectorAll("img[data-index]");

  for (let i = 0, l = state.value.images.length; i < l; i++) {
    const item = state.value.images[i];

    if (selectImages.value.length && !item.select) {
      continue;
    }

    try {
      const resp = await fetch(item.url);
      const blob = await resp.blob();
      item.downloaded = true;
      zip.file(item.filename, blob);
      // 每下载 k 张图片就滚动到对应图片的位置
      if (i > 0 && i % 5 === 0) {
        nextTick(() => {
          imageEls[i] &&
            imageEls[i].scrollIntoView({
              behavior: "smooth",
            });
        });
      }
    } catch (e) {
      console.error(e);
    }
  }

  zip.file("info.txt", generatePackInfoText());
  await zip.downloadAsync(`${state.value.title}.zip`);

  state.value.downloading = false;
};

const loadData = async () => {
  if (itemType.value === "ip" || itemType.value === "up") {
    await loadSuit();
  } else {
    await loadCollection();
  }
};

loadData();

const emit = defineEmits(["close", "search-emoji"]);

const close = () => {
  emit("close");
};

const searchEmoji = () => {
  close();
  emit("search-emoji", state.value.title);
};
</script>

<style scoped>
.image-grid-item {
  @apply relative;
}

.image-grid-item.select .select-pointer {
  @apply absolute top-[-5px] right-[-5px] w-[15px] h-[15px] rounded-full bg-green-400;
}

.image-grid-item .video-pointer {
  @apply absolute top-[0px] left-[0px] px-[2px] py-[1px] rounded-br-md text-sm  text-white bg-slate-600/55;
}
</style>
