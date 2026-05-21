<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useVaultStore, type Vault } from '../stores/vault'
import { useSecretStore } from '../stores/secret'
import { useAuthStore } from '../stores/auth'
import SecretListItem from '../components/SecretListItem.vue'
import SecretModal from '../components/modals/SecretModal.vue'
import MasterKeyRequiredModal from '../components/modals/MasterKeyRequiredModal.vue'

const route = useRoute()
const router = useRouter()
const vaultStore = useVaultStore()
const secretStore = useSecretStore()
const authStore = useAuthStore()

const vaultId = route.params.id as string
const vault = ref<Vault | null>(null)
const secrets = ref<any[]>([])
const isLoading = ref(true)
const isSecretModalOpen = ref(false)
const isMasterKeyModalOpen = ref(false)

onMounted(async () => {
  try {
    const [vaultData, secretsData] = await Promise.all([
      vaultStore.fetchVaultById(vaultId),
      secretStore.fetchSecretsByVaultId(vaultId)
    ])
    vault.value = vaultData
    secrets.value = secretsData
  } catch (error) {
    console.error('Failed to load vault details:', error)
    router.push('/dashboard/vaults')
  } finally {
    isLoading.value = false
  }
})

const handleSecretCreated = async () => {
  secrets.value = await secretStore.fetchSecretsByVaultId(vaultId)
}

const openAddSecret = () => {
  if (!authStore.hasMasterKey) {
    isMasterKeyModalOpen.value = true
    return
  }
  isSecretModalOpen.value = true
}
</script>

<template>
  <div class="space-y-8 max-w-6xl mx-auto px-4 md:px-8 py-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-4">
        <button 
          @click="router.push('/dashboard/vaults')"
          class="flex items-center space-x-2 text-zinc-500 hover:text-white transition-colors text-sm font-medium group"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
          <span>Back to Vaults</span>
        </button>

        <div v-if="vault" class="space-y-2">
          <div class="flex items-center space-x-3">
             <div class="w-10 h-10 bg-emerald-500/10 rounded-xl flex items-center justify-center border border-emerald-500/20">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-400"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
             </div>
             <h1 class="text-3xl font-bold tracking-tight text-white">{{ vault.name }}</h1>
          </div>
          <p class="text-zinc-500 text-base max-w-2xl">{{ vault.description || 'No description provided for this vault.' }}</p>
        </div>
      </div>

      <button 
        @click="openAddSecret"
        class="button-primary flex items-center space-x-2 px-6 py-2.5 h-fit"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
        <span>Add Secret</span>
      </button>
    </div>

    <!-- Secrets List -->
    <div v-if="isLoading" class="space-y-4 animate-pulse">
      <div v-for="i in 4" :key="i" class="h-20 bg-zinc-900/50 rounded-2xl border border-zinc-900"></div>
    </div>

    <div v-else-if="secrets.length === 0" class="flex flex-col items-center justify-center py-20 border border-dashed border-zinc-900 rounded-3xl space-y-4">
      <div class="w-16 h-16 bg-zinc-950 rounded-full flex items-center justify-center border border-zinc-900 text-zinc-700">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      </div>
      <div class="text-center">
        <h3 class="text-white">This vault is empty</h3>
        <p class="text-zinc-500 text-sm max-w-xs mx-auto mt-2">Start adding logins, API keys or sensitive notes to this container.</p>
      </div>
      <button @click="isSecretModalOpen = true" class="button-primary text-sm mt-4">Add First Secret</button>
    </div>

    <div v-else class="grid grid-cols-1 gap-4">
      <SecretListItem 
        v-for="secret in secrets" 
        :key="secret.id" 
        :secret="secret" 
        @request-master-key="isMasterKeyModalOpen = true"
      />
    </div>

    <SecretModal 
      :is-open="isSecretModalOpen" 
      :preselected-vault-id="vaultId"
      @close="isSecretModalOpen = false" 
      @created="handleSecretCreated"
    />

    <MasterKeyRequiredModal
      :show="isMasterKeyModalOpen"
      @close="isMasterKeyModalOpen = false"
    />
  </div>
</template>
