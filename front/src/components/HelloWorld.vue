<script setup lang="ts">
import { ref } from 'vue'
const message = ref("hello" )
</script>

<template>
  <p class="text-red-500">{{ message }}</p>
</template>
