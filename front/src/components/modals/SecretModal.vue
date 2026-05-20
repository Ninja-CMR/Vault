<script setup lang="ts">
import { ref } from 'vue'
import { useSecretStore } from '../../stores/secret'
import { useVaultStore } from '../../stores/vault'
import { useDashboard } from '../../composables/useDashboard'

const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits(['close'])

const secretStore = useSecretStore()
const vaultStore = useVaultStore()
const { fetchDashboardData } = useDashboard()

const title = ref('')
const type = ref<'LOGIN' | 'API_KEY' | 'TOKEN' | 'NOTE'>('LOGIN')
const description = ref('')
const selectedVaultId = ref('')

// Secret fields based on type
const fields = ref({
  email: '',
  password: '',
  api_key: '',
  token: '',
  note: ''
})

const isSubmitting = ref(false)

const handleClose = () => {
  title.value = ''
  description.value = ''
  emit('close')
}

const handleSubmit = async () => {
  if (!title.value || !selectedVaultId.value) return
  
  isSubmitting.value = true
  try {
    let payload = {}
    if (type.value === 'LOGIN') payload = { email: fields.value.email, password: fields.value.password }
    else if (type.value === 'API_KEY') payload = { api_key: fields.value.api_key }
    else if (type.value === 'TOKEN') payload = { token: fields.value.token }
    else if (type.value === 'NOTE') payload = { note: fields.value.note }

    await secretStore.createSecret(
      selectedVaultId.value,
      title.value,
      type.value,
      payload,
      description.value
    )
    await fetchDashboardData() // Refresh stats
    handleClose()
  } catch (error) {
    console.error(error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0 scale-95"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95"
  >
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div class="w-full max-w-lg card-resend !p-0 shadow-[0_0_50px_rgba(0,0,0,0.5)] relative overflow-hidden">
        <!-- Close Button -->
        <button 
          @click="handleClose"
          class="absolute top-6 right-6 p-2 text-zinc-600 hover:text-white transition-colors z-10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </button>

        <div class="p-10 space-y-8">
          <div class="space-y-2">
            <h3 class="text-2xl font-bold tracking-tight text-white">Add Secret</h3>
            <p class="text-zinc-500 text-sm">Everything is encrypted on your device before being stored.</p>
          </div>

          <!-- Master Key Warning -->
          <div v-if="!secretStore.masterPassword" class="p-3 rounded-lg bg-orange-500/10 border border-orange-500/20 flex items-center space-x-3">
             <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-orange-500 shrink-0"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
             <p class="text-[12px] text-orange-200 font-medium leading-tight">
               Please set your <span class="text-white">Master Key</span> in the sidebar to secure this secret.
             </p>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div class="grid grid-cols-2 gap-4">
               <div class="space-y-1.5">
                  <label class="text-[13px] font-medium text-zinc-400">Vault</label>
                  <select v-model="selectedVaultId" class="input-resend w-full" required>
                    <option disabled value="">Select a vault</option>
                    <option v-for="vault in vaultStore.vaults" :key="vault.id" :value="vault.id">
                      {{ vault.name }}
                    </option>
                  </select>
               </div>
               <div class="space-y-1.5">
                  <label class="text-[13px] font-medium text-zinc-400">Type</label>
                  <select v-model="type" class="input-resend w-full">
                    <option value="LOGIN">Login</option>
                    <option value="API_KEY">API Key</option>
                    <option value="TOKEN">Token</option>
                    <option value="NOTE">Secure Note</option>
                  </select>
               </div>
            </div>

            <div class="space-y-1.5">
              <label class="text-[13px] font-medium text-zinc-400">Title</label>
              <input v-model="title" type="text" placeholder="e.g. My Facebook Account" class="input-resend w-full" required />
            </div>

            <!-- Dynamic Fields -->
            <div v-if="type === 'LOGIN'" class="grid grid-cols-1 gap-4">
              <div class="space-y-1.5">
                <label class="text-[13px] font-medium text-zinc-400">Email / Username</label>
                <input v-model="fields.email" type="text" class="input-resend w-full" placeholder="john@example.com" />
              </div>
              <div class="space-y-1.5">
                <label class="text-[13px] font-medium text-zinc-400">Password</label>
                <input v-model="fields.password" type="password" class="input-resend w-full" placeholder="••••••••" />
              </div>
            </div>

            <div v-else-if="type === 'API_KEY'" class="space-y-1.5">
              <label class="text-[13px] font-medium text-zinc-400">API Key</label>
              <input v-model="fields.api_key" type="password" class="input-resend w-full" placeholder="sk-..." />
            </div>

            <div v-else-if="type === 'TOKEN'" class="space-y-1.5">
              <label class="text-[13px] font-medium text-zinc-400">Token</label>
              <textarea v-model="fields.token" class="input-resend w-full h-24 py-3" placeholder="eyJhbGci..."></textarea>
            </div>

            <div v-else-if="type === 'NOTE'" class="space-y-1.5">
              <label class="text-[13px] font-medium text-zinc-400">Note</label>
              <textarea v-model="fields.note" class="input-resend w-full h-32 py-3" placeholder="Super secret stuff..."></textarea>
            </div>

            <div class="pt-6">
              <button 
                type="submit" 
                class="button-primary w-full py-3 text-[14px] font-bold" 
                :disabled="isSubmitting || !secretStore.masterPassword"
              >
                {{ isSubmitting ? 'Stashing...' : 'Add Secret' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </transition>
</template>
