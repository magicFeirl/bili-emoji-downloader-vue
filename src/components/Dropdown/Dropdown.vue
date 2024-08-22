<template>
  <div ref="dropdownBodyRef" class="relative z-50">
    <div>
      <slot name="dropdown"></slot>
    </div>
    <div
      v-if="props.modelValue"
      class="absolute right-0 flex flex-col dropdown-body"
    >
      <slot name="dropdown-body"></slot>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from "vue";

const props = defineProps({
  // 是否显示 dropdown
  modelValue: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue"]);

const dropdownBodyRef = ref();

const close = () => {
  emit("update:modelValue", false);
};

const clickHandler = (e) => {
  const { target } = e;
  const dropdownEl = dropdownBodyRef.value;

  if (dropdownEl.contains(target)) {
    return;
  }

  close();
};

onMounted(() => {
  window.addEventListener("click", clickHandler);
});

onBeforeUnmount(() => {
  window.removeEventListener("click", clickHandler);
});
</script>

<style scoped>
.dropdown-body {
  @apply shadow-md bg-white;
}

:slotted(.dropdown-body > div) {
  @apply py-2 px-1 flex w-full items-center;
}
</style>
