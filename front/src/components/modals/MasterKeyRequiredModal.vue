<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps<{
  show: boolean
}>()

const emit = defineEmits(['close'])

const goToSetup = () => {
  emit('close')
  router.push('/setup-master-key')
}
</script>

<template>
  <div v-if="show" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black/60 backdrop-blur-md" @click="$emit('close')"></div>
    
    <!-- Modal -->
    <div class="relative w-full max-w-sm card-resend p-8 space-y-6 shadow-[0_0_50px_rgba(0,0,0,0.5)] border-white/10 animate-scale-in">
      <div class="text-center space-y-4">
        <div class="mx-auto w-14 h-14 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber-500">
            <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>
          </svg>
        </div>
        
        <div class="space-y-1">
          <h3 class="text-lg font-bold text-white">Master Key Required</h3>
          <p class="text-zinc-500 text-xs leading-relaxed">
            You need to set up your Master Key before you can create vaults or secrets. 
            This ensures your data is end-to-end encrypted.
          </p>
        </div>
      </div>

      <div class="flex flex-col space-y-3">
        <button 
          @click="goToSetup"
          class="button-primary w-full py-2.5 text-xs font-bold"
        >
          Set Up Master Key Now
        </button>
        <button 
          @click="$emit('close')"
          class="w-full py-2.5 text-[11px] font-medium text-zinc-500 hover:text-white transition-colors"
        >
          Maybe Later
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
