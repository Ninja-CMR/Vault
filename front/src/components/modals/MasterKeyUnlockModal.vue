<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

const props = defineProps<{
  show: boolean
}>()

const emit = defineEmits(['close', 'unlocked'])
const authStore = useAuthStore()

const password = ref('')
const isLoading = ref(false)
const error = ref('')
const showPassword = ref(false)

const handleUnlock = async () => {
  if (!password.value) return
  
  isLoading.value = true
  error.value = ''
  
  try {
    await authStore.unlockMasterKey(password.value)
    password.value = ''
    emit('unlocked')
    emit('close')
  } catch (e: any) {
    error.value = e.message || "Mot de passe incorrect"
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div v-if="show" class="fixed inset-0 z-[70] flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="$emit('close')"></div>
    
    <!-- Modal -->
    <div class="relative w-full max-w-sm card-resend p-8 space-y-6 shadow-[0_0_50px_rgba(0,0,0,0.5)] border-white/10 animate-scale-in">
      <div class="text-center space-y-4">
        <div class="mx-auto w-14 h-14 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500">
            <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
        </div>
        
        <div class="space-y-1">
          <h3 class="text-lg font-bold text-white">Unlock Vault</h3>
          <p class="text-zinc-500 text-xs leading-relaxed">
            Enter your account password to unlock your Master Key and access your secrets.
          </p>
        </div>
      </div>

      <div class="space-y-4">
        <div class="space-y-1.5">
          <div class="relative">
            <input 
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Enter password..."
              class="input-resend w-full py-2.5 pr-10 text-sm"
              @keyup.enter="handleUnlock"
              autofocus
            />
            <button 
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-600 hover:text-zinc-400 p-1"
            >
                <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0z"/><circle cx="12" cy="12" r="3"/><path d="m17.5 17.5 2.5 2.5"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" x2="22" y1="2" y2="22"/></svg>
            </button>
          </div>
          <p v-if="error" class="text-[10px] text-red-500 font-medium px-1">{{ error }}</p>
        </div>

        <button 
          @click="handleUnlock"
          :disabled="isLoading || !password"
          class="button-primary w-full py-2.5 text-xs font-bold flex items-center justify-center space-x-2"
        >
          <svg v-if="isLoading" class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
          <span v-else>Unlock Master Key</span>
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
