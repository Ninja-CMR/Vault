<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const router = useRouter()

const password = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)
const error = ref('')
const success = ref(false)

const handleGenerate = async () => {
    if (password.value.length < 8) {
        error.value = "Le mot de passe doit faire au moins 8 caractères."
        return
    }

    error.value = ''
    isLoading.value = true

    try {
        const response = await axios.post('http://localhost:8000/security/master-key/generate', 
            { 
                password: password.value,
                force_regenerate: authStore.hasMasterKey
            },
            { headers: { Authorization: `Bearer ${authStore.token}` } }
        )
        success.value = true
        authStore.hasMasterKey = true
        authStore.setMasterKey(response.data.master_key, response.data.public_token)
        localStorage.setItem('vault_has_master_key', 'true')
        
        setTimeout(() => {
            router.push('/dashboard')
        }, 2000)
    } catch (e: any) {
        error.value = e.response?.data?.detail || "Une erreur est survenue lors de la génération."
    } finally {
        isLoading.value = false
    }
}

// onMounted redirect removed to allow regeneration/fixing tokens.
</script>

<template>
  <div class="min-h-screen bg-black flex items-center justify-center p-6 bg-gradient-to-br from-black via-zinc-950 to-emerald-950/20">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center space-y-4">
        <div class="mx-auto w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shadow-[0_0_30px_rgba(16,185,129,0.1)]">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500">
            <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
        </div>
        <h1 class="text-3xl font-bold tracking-tight text-white">Master Key Setup</h1>
        <p class="text-zinc-400 text-sm max-w-xs mx-auto leading-relaxed">
          Your Master Key is required to encrypt and decrypt your vault data. 
          We'll derive it from your password using a secure mechanism.
        </p>
      </div>

      <!-- Card -->
      <div class="card-resend p-8 space-y-6">
        <div v-if="!success" class="space-y-6">
          <div class="space-y-1.5">
            <label class="text-[11px] font-semibold text-zinc-500 uppercase tracking-widest ml-1">Current Password</label>
            <div class="relative">
              <input 
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                class="input-resend w-full py-3 pr-10"
              />
              <button 
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-600 hover:text-zinc-400 p-1"
              >
                  <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0z"/><circle cx="12" cy="12" r="3"/><path d="m17.5 17.5 2.5 2.5"/></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" x2="22" y1="2" y2="22"/></svg>
              </button>
            </div>
          </div>

          <button 
            @click="handleGenerate"
            :disabled="!password || isLoading"
            class="w-full group relative overflow-hidden bg-white text-black font-bold py-3.5 rounded-xl transition-all active:scale-[0.98]"
            :class="authStore.hasMasterKey ? 'bg-amber-500 text-black' : 'hover:shadow-[0_0_20px_rgba(255,255,255,0.1)]'"
          >
            <div class="relative z-10 flex items-center justify-center space-x-2">
              <svg v-if="isLoading" class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
              <span v-else>{{ authStore.hasMasterKey ? 'Régénérer la Master Key' : 'Générer la Master Key' }}</span>
              <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:translate-x-0.5 transition-transform"><path d="M5 12h14m-7-7 7 7-7 7"/></svg>
            </div>
          </button>

          <p v-if="error" class="text-xs text-red-500 text-center animate-shake">{{ error }}</p>
        </div>

        <!-- Success State -->
        <div v-else-if="success" class="space-y-8 animate-in fade-in zoom-in duration-500">
            <div class="text-center space-y-4">
                <div class="mx-auto w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                </div>
                <div class="space-y-1">
                    <h2 class="text-2xl font-bold text-white">Vault Secured</h2>
                    <p class="text-zinc-400 text-sm">Your Master Key has been generated successfully.</p>
                </div>
            </div>

            <div class="bg-emerald-500/5 border border-emerald-500/10 rounded-xl p-6 space-y-4">
                <div class="space-y-1">
                    <span class="text-[10px] uppercase tracking-wider font-bold text-emerald-500/50">Your Vault Access Code</span>
                    <div class="flex items-center justify-between bg-black/40 border border-white/5 rounded-lg p-3">
                        <code class="text-lg font-mono text-emerald-500">{{ authStore.publicToken }}</code>
                        <button class="text-zinc-500 hover:text-white transition-colors" title="Copy code">
                             <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                        </button>
                    </div>
                </div>
                <p class="text-[11px] text-zinc-500 leading-relaxed italic">
                    Use this code to identify your secure session. Your real master key is hidden for your protection.
                </p>
            </div>

            <p class="text-center text-xs text-zinc-500 animate-pulse">Redirecting to your dashboard...</p>
        </div>
      </div>

      <!-- Security Notice -->
      <div class="text-center">
        <div class="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-zinc-900/50 border border-zinc-800 text-[10px] text-zinc-500 uppercase tracking-widest font-mono">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>End-to-End Encryption Active</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-shake {
  animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
}
@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}
.animate-fade-in { animation: fadeIn 0.3s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
