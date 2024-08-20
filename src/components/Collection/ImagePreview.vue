<template>
  <div
    @click="emit('update:modelValue', false)"
    v-if="modelValue"
    class="z-20 bg-black/70 fixed top-0 left-0 w-full h-full flex justify-center items-center"
  >
    <img class="max-h-full w-auto" :src="src" alt="Image" />
  </div>
</template>

<script setup>
const props = defineProps({
  src: String,
  modelValue: Boolean,
});

const emit = defineEmits(["update:modelValue"]);
</script>

<style lang="scss" scoped></style>
