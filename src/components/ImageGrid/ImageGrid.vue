<template>
  <section
    class="emoji-pack card-shadow my-2 p-4 rounded-md border ring-1 ring-inset ring-slate-50 relative"
    :class="state.expanded ? 'pb-2' : 'pb-[36px]'"
  >
    <!-- header -->
    <div class="flex mb-4 pb-1 items-center">
      <p class="text-lg text-gray-800 hover:text-blue-400 transition-colors">
        <a :href="item_url" target="_blank">
          {{ title }}({{ imageList.length }})
        </a>
      </p>
      <div class="flex-1"></div>
      <label :class="state.tojpg ? 'text-blue-400' : ''" for="tojpg"
        >转为JPG</label
      >
      <input v-model="state.tojpg" type="checkbox" id="tojpg" class="mx-2" />
      <button
        title="下载"
        :disabled="state.downloading"
        class="download -mt-2 disabled:text-gray-300"
        @click="downloadAll()"
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

      <button
        title="搜索装扮/收藏集"
        class="ml-2 -mt-1"
        @click="handleSearchSuit"
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
            d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"
          />
        </svg>
      </button>
    </div>
    <!-- content -->
    <div
      class="grid grid-cols-4 gap-2 overflow-hidden py-1 transition-all"
      :class="state.expanded ? 'h-auto' : 'sm:h-[265px] h-[255px]'"
    >
      <div v-for="e in imageList" :key="e.id">
        <div
          class="emote-image relative flex justify-center p-1 overflow-hidden"
        >
          <img
            :data-id="e.id"
            v-lazy
            class="transition-all w-[120px] h-auto object-contain"
            :class="
              e.dlProgress === 100
                ? 'rounded  ring-1 ring-green-500'
                : e.dlProgress === '-1'
                ? 'rounded ring-1 ring-red-500'
                : ''
            "
            :data-src="e.url"
            :alt="e.text"
          />
          <!-- download single -->
          <div
            @click="downloadSingle(e, true)"
            class="emote-image-bottom transition-all absolute -bottom-[1.25rem] bg-gray-600/50 w-full flex justify-center h-5"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-4 text-white"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
    <div
      @click="expandCard()"
      v-if="imageList.length > 8 && !state.expanded"
      class="absolute bottom-0 left-0 cursor-pointer w-full flex justify-center text-slate-300 bg-gradient-to-b from-transparent to-slate-100"
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
          d="m19.5 8.25-7.5 7.5-7.5-7.5"
        />
      </svg>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { saveAs } from "file-saver";

import * as API from "@/api";

import { vLazy } from "@/directives/lazy.js";
import useJSZip from "@/utils/useJSZip.js";
import useInfoHeader from "@/utils/useInfoHeader.js";

onMounted(() => {
  window.addEventListener("resize", async (e) => {
    // PC 接口只有 10 条数据，宽度过小时自动展开卡片
    if (props.type.apiType === "pc" && window.innerWidth < 540) {
      await expandCard();
    }
  });
});

const props = defineProps({
  // pack: API 接口返回的原始数据结构
  pack: {
    type: Object,
    required: true,
  },
  item_url: {
    type: String,
  },
  // 标题
  title: {
    type: String,
    required: true,
  },
  imageList: {
    type: Array,
    required: true,
    validator: (value) => {
      return true;
    },
  },
  // type: { apiType: 'pc' | 'app', emoteType: 'emote' | 'liveroom'}
  type: {
    type: Object,
    required: true,
  },
});

const state = ref({
  tojpg: true,
  expanded: false,
  downloading: false,
});

const imageList = ref([...props.imageList]);

const downloadSingle = async (e, save = false) => {
  const resp = await fetch(e.url.replace("http:", location.protocol));
  const { tojpg } = state.value;
  const filename =
    e.text + (tojpg ? ".jpg" : e.url.slice(e.url.lastIndexOf(".")));
  const blob = await resp.blob();

  const img = new Image();
  img.src = URL.createObjectURL(blob);

  return await new Promise((resolve) => {
    img.onload = () => {
      if (tojpg) {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
        canvas.toBlob(
          (blob) => {
            resolve(blob);
            URL.revokeObjectURL(img.src);
          },
          "image/jpeg",
          1
        );
      } else {
        resolve(blob);
      }
    };

    e.dlProgress = 100;
  }).then((blob) => {
    if (save) {
      saveAs(blob, filename);
    } else {
      return { blob, filename };
    }
  });
};

const downloadAll = async () => {
  const generatePackInfoText = () => {
    return useInfoHeader({
      name: props.title,
      jumplink: props.item_url,
      urls: imageList.value.map((e) => ({ name: e.text, url: e.url })),
    });
  };

  state.value.downloading = true;

  await expandCard();

  const zip = new useJSZip();
  for (const e of imageList.value) {
    try {
      const { filename, blob } = await downloadSingle(e, false);
      zip.file(filename, blob);
    } catch (e) {
      e.dlProgress = -1;
      console.error(e);
    }
  }

  zip.file("info.txt", generatePackInfoText());

  await zip.downloadAsync(props.title);

  state.value.downloading = false;
};

const expandCard = async () => {
  if (state.value.expanded) {
    return;
  }

  const loadPackForPC = async () => {
    if (props.type.apiType === "pc") {
      const data = await API.getEmojiDetailById(props.pack.id);
      imageList.value = data.data.package.emotes;
    }
  };

  await loadPackForPC();

  state.value.expanded = true;
};

const emit = defineEmits(["search-suit"]);
const handleSearchSuit = () => {
  emit("search-suit", props.title);
};
</script>

<style scoped>
.emote-image:hover > .emote-image-bottom {
  cursor: pointer;
  bottom: 0;
}

.card-shadow {
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.15);
}
</style>
