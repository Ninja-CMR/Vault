<script setup lang="ts">
import { ref } from 'vue'
import { useSecretStore, type Secret } from '../stores/secret'
import { useAuthStore } from '../stores/auth'

const props = defineProps<{
  secret: Secret
}>()

const secretStore = useSecretStore()
const isRevealed = ref(false)
const decryptedData = ref<any>(null)
const isLoading = ref(false)
const countdown = ref(15)
let timer: any = null
const emit = defineEmits(['request-master-key'])

const authStore = useAuthStore()
const handleReveal = async () => {
  if (!authStore.masterKey) {
    emit('request-master-key')
    return
  }
  
  if (isRevealed.value) {
    hideSecret()
    return
  }

  isLoading.value = true
  try {
    decryptedData.value = await secretStore.revealSecret(props.secret.id)
    isRevealed.value = true
    startTimer()
  } catch (error: any) {
    alert(error.message || 'Échec de la révélation du secret.')
  } finally {
    isLoading.value = false
  }
}

const startTimer = () => {
  countdown.value = 15
  if (timer) clearInterval(timer)
  timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      hideSecret()
    }
  }, 1000)
}

const hideSecret = () => {
  isRevealed.value = false
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  countdown.value = 15
}
const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text)
  // Could add a toast here
}
</script>

<template>
  <div class="card-resend !p-4 hover:bg-zinc-900/10 transition-colors group">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <div class="w-10 h-10 bg-zinc-900 rounded-lg flex items-center justify-center border border-zinc-800">
          <svg v-if="secret.type === 'LOGIN'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-400 group-hover:text-emerald-500/50 transition-colors"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <svg v-else-if="secret.type === 'API_KEY'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-400 group-hover:text-emerald-500/50 transition-colors"><path d="m21 2-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3v-3z"/></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-400 group-hover:text-emerald-500/50 transition-colors"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
        </div>
        <div>
          <h5 class="text-[14px] font-bold text-white">{{ secret.title }}</h5>
          <p class="text-[12px] text-zinc-500">{{ secret.type }} • {{ secret.description || 'No description' }}</p>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <div v-if="isRevealed" class="flex items-center space-x-2">
           <div class="relative w-6 h-6 flex items-center justify-center">
             <svg class="w-full h-full -rotate-90">
               <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2" class="text-zinc-900" />
               <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2" class="text-emerald-500 transition-all duration-1000" :stroke-dasharray="62.8" :stroke-dashoffset="62.8 * (1 - countdown / 15)" />
             </svg>
             <span class="absolute text-[9px] font-bold text-emerald-400">{{ countdown }}</span>
           </div>
        </div>
        
        <button 
          @click="handleReveal"
          class="text-[12px] font-bold px-4 py-1.5 rounded-lg transition-all"
          :class="isRevealed ? 'bg-zinc-800 text-zinc-400 hover:text-white border border-zinc-700' : 'button-primary !py-1.5'"
        >
          <span v-if="isLoading">Loading...</span>
          <span v-else-if="isRevealed">Hide</span>
          <span v-else>Reveal</span>
        </button>
      </div>
    </div>

    <!-- Revealed Content -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
    >
      <div v-if="isRevealed" class="mt-4 p-4 rounded-xl bg-zinc-950/50 border border-zinc-900/50 space-y-3 backdrop-blur-sm">
        <div v-for="(val, key) in decryptedData" :key="key" class="flex flex-col space-y-1">
          <label class="text-[10px] uppercase tracking-wider font-bold text-zinc-600">{{ key }}</label>
          <div class="flex items-center justify-between group/row">
            <code class="text-[13px] text-zinc-300 font-mono">{{ val }}</code>
            <button @click="copyToClipboard(val)" class="p-1 hover:text-emerald-400 text-zinc-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>
