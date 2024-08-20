<template>
  <div
    @click="openImagePreview"
    class="flex flex-col rounded-md overflow-hidden justify-between"
  >
    <div class="flex-1">
      <img
        class="object-cover h-full"
        :src="`${data.properties.image_cover}@328w_360h_1o.webp`"
        :alt="data.name"
      />
    </div>
    <div class="mt-2 font-bold line-clamp-1">{{ data.name }}</div>
  </div>

  <CollectionImagePreview
    :data="data"
    @close="closeImagePreview"
    v-if="state.preview"
  ></CollectionImagePreview>
</template>

<script setup>
import { ref } from "vue";

import CollectionImagePreview from "@/components/Collection/CollectionImagePreview.vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const data = ref({ ...props.data });

const state = ref({
  preview: false,
});

const openImagePreview = () => {
  document.body.style.overflow = "hidden";
  state.value.preview = true;
};

const closeImagePreview = () => {
  state.value.preview = false;
  document.body.style.overflow = "auto";
};
</script>

<style lang="scss" scoped></style>
