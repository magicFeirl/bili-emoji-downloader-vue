<template>
  <div
    ref="imagePreviewBoxRef"
    @click="emit('update:modelValue', false)"
    v-if="modelValue"
    class="z-20 bg-black/70 fixed top-0 left-0 w-full h-full"
  >
    <div class="w-full h-full flex justify-center items-center">
      <template v-if="video">
        <video class="max-h-full" loop @click.stop :src="src" autoplay muted controls></video>
      </template>
      <template v-else>
        <img
          @click.stop="toggleZoom($event)"
          class="max-h-full w-auto"
          :class="zoomState.zoomIn ? 'cursor-zoom-out' : 'cursor-zoom-in'"
          :src="src"
          :alt="src"
        />
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";

const props = defineProps({
  src: String,
  modelValue: Boolean,
  video: Boolean,
});

const emit = defineEmits(["update:modelValue"]);

const imagePreviewBoxRef = ref();

const zoomState = ref({
  scale: 1.5,
  zoomIn: false,
});

const toggleZoom = (e) => {
  const zoomIn = (zoomState.value.zoomIn = !zoomState.value.zoomIn);
  const { offsetX: x, offsetY: y } = e;
  const imgEl = e.target;

  if (zoomIn) {
    Object.assign(imgEl.style, {
      transform: `scale(${zoomState.value.scale})`,
      "transform-origin": `${x}px ${y}px`,
      margin: `${y}px 0 0 0`,
    });

    nextTick(() => {
      imagePreviewBoxRef.value.scrollTo(x, y);
    });
  } else {
    imgEl.style = ``;
  }

  imagePreviewBoxRef.value.style.overflow = zoomIn ? "auto" : "hidden";
};
</script>

<style lang="scss" scoped></style>
