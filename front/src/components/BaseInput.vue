<script setup lang="ts">
import { ref, computed } from 'vue'
import { useField } from 'vee-validate'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
  }
})

const { value, errorMessage, handleBlur, handleChange, meta } = useField(() => props.name, undefined, {
  initialValue: ''
})

const isPasswordVisible = ref(false)

const inputType = computed(() => {
  if (props.type === 'password') {
    return isPasswordVisible.value ? 'text' : 'password'
  }
  return props.type
})

const toggleVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value
}
</script>

<template>
  <div class="space-y-1.5 w-full text-left">
    <label :for="name" class="block text-[13px] font-medium text-zinc-400">
      {{ label }}
    </label>
    <div class="relative">
      <input
        :id="name"
        :type="inputType"
        :placeholder="placeholder"
        v-model="value"
        @blur="handleBlur"
        @input="handleChange"
        class="input-resend w-full pr-10 text-[14px]"
        :class="{ '!border-error': !!errorMessage && meta.touched }"
      />
      
      <!-- Visibility Toggle for Password Fields -->
      <button
        v-if="type === 'password'"
        type="button"
        @click="toggleVisibility"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-white transition-colors focus:outline-none"
      >
        <svg v-if="isPasswordVisible" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" x2="22" y1="2" y2="22"/></svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0z"/><circle cx="12" cy="12" r="3"/></svg>
      </button>

      <!-- Validation Status -->
      <div v-else-if="meta.valid && value" class="absolute right-3 top-1/2 -translate-y-1/2 text-success">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
    </div>
    <p v-if="errorMessage && meta.touched" class="text-[12px] text-error mt-1 px-1">
      {{ errorMessage }}
    </p>
  </div>
</template>
