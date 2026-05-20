<script setup lang="ts">
import { ref } from 'vue'
import { useVaultStore } from '../../stores/vault'
import { useDashboard } from '../../composables/useDashboard'

const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits(['close'])

const vaultStore = useVaultStore()
const { fetchDashboardData } = useDashboard()
const name = ref('')
const description = ref('')
const isSubmitting = ref(false)

const handleClose = () => {
  name.value = ''
  description.value = ''
  emit('close')
}

const handleSubmit = async () => {
  if (!name.value) return
  
  isSubmitting.value = true
  try {
    await vaultStore.createVault(name.value, description.value)
    await fetchDashboardData()
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
      <div class="w-full max-w-md card-resend !p-0 shadow-[0_0_50px_rgba(0,0,0,0.5)] relative overflow-hidden">
        <!-- Close Button -->
        <button 
          @click="handleClose"
          class="absolute top-4 right-4 p-2 text-zinc-600 hover:text-white transition-colors z-10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </button>

        <div class="p-8 space-y-6">
          <div class="space-y-2">
            <h3 class="text-2xl font-bold tracking-tight text-white">New Vault</h3>
            <p class="text-zinc-500 text-sm">Create a container to organize your secrets.</p>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-5">
            <div class="space-y-1.5">
              <label class="text-[13px] font-medium text-zinc-400">Vault Name</label>
              <input 
                v-model="name"
                type="text" 
                placeholder="e.g. Work, Personal, APIs..."
                class="input-resend w-full"
                required
                autofocus
              />
            </div>

            <div class="space-y-1.5">
              <label class="text-[13px] font-medium text-zinc-400">Description (optional)</label>
              <textarea 
                v-model="description"
                placeholder="What's inside this vault?"
                class="input-resend w-full min-h-[100px] resize-none py-3"
              ></textarea>
            </div>

            <div class="pt-4">
              <button 
                type="submit" 
                class="button-primary w-full py-2.5 text-[14px] font-semibold"
                :disabled="!name || isSubmitting"
              >
                {{ isSubmitting ? 'Creating...' : 'Create Vault' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </transition>
</template>
