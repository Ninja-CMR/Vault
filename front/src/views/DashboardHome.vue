<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useDashboard } from '../composables/useDashboard'
import { useVaultStore } from '../stores/vault'
import { useSecretStore } from '../stores/secret'
import { formatDate } from '../utils/format'
import VaultModal from '../components/modals/VaultModal.vue'
import SecretModal from '../components/modals/SecretModal.vue'
import SecretListItem from '../components/SecretListItem.vue'

const { stats, fetchDashboardData } = useDashboard()
const vaultStore = useVaultStore()
const secretStore = useSecretStore()
const isVaultModalOpen = ref(false)
const isSecretModalOpen = ref(false)

const recentSecrets = computed(() => secretStore.secrets.slice(0, 4))

onMounted(async () => {
  console.log('Dashboard mounting...')
  try {
    await Promise.all([
      fetchDashboardData(),
      vaultStore.fetchVaults(),
      secretStore.fetchAllSecrets()
    ])
    console.log('Dashboard data loaded:', {
       vaults: vaultStore.vaults.length,
       secrets: secretStore.secrets.length
    })
  } catch (err) {
    console.error('Failed to load dashboard:', err)
  }
})
</script>

<template>
  <div class="p-8 space-y-12 max-w-7xl mx-auto">
    <!-- Page Header -->
    <div class="flex flex-col space-y-8">
      <div class="flex items-end justify-between">
        <div class="space-y-1">
          <h2 class="text-3xl font-bold tracking-tight text-white">Overview</h2>
          <p class="text-zinc-500 text-sm">Security at a glance.</p>
        </div>
        <div class="flex items-center space-x-3">
           <button 
             @click="isSecretModalOpen = true"
             class="button-secondary text-[13px] py-2 px-5 flex items-center space-x-2"
           >
             <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
             <span>Add Secret</span>
           </button>
           <button 
             @click="isVaultModalOpen = true"
             class="button-primary text-[13px] py-2 px-5 flex items-center space-x-2"
           >
             <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
             <span>New Vault</span>
           </button>
        </div>
      </div>

      <!-- Filters / Tabs -->
      <div class="flex items-center justify-between border-b border-zinc-800/50 pb-px">
        <div class="flex items-center space-x-6">
          <button class="text-[13px] font-medium border-b-2 border-white pb-3 text-white">Overview</button>
        </div>
        <div class="flex items-center space-x-4 pb-3">
          <div class="relative">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-600"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            <input type="text" placeholder="Search..." class="bg-zinc-900 border border-border rounded-lg pl-8 pr-3 py-1.5 text-[13px] w-64 focus:outline-none focus:border-zinc-700 placeholder:text-zinc-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card-resend group">
        <div class="flex items-center justify-between mb-2">
          <span class="text-[12px] font-medium text-zinc-500">Total Vaults</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-600"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        </div>
        <div class="flex items-baseline space-x-2">
          <h3 class="text-2xl font-bold">{{ stats.vaults_count || 0 }}</h3>
        </div>
      </div>

      <div class="card-resend">
        <div class="flex items-center justify-between mb-2">
          <span class="text-[12px] font-medium text-zinc-500">Active Secrets</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-600"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3v-3h-3z"/></svg>
        </div>
        <div class="flex items-baseline space-x-2">
          <h3 class="text-2xl font-bold">{{ stats.secrets_count || 0 }}</h3>
          <span class="text-[11px] text-zinc-500 font-medium">Synced everywhere</span>
        </div>
      </div>

      <div class="card-resend">
        <div class="flex items-center justify-between mb-2">
          <span class="text-[12px] font-medium text-zinc-500">Passwords Generated</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-600"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></svg>
        </div>
        <div class="flex items-baseline space-x-2">
          <h3 class="text-2xl font-bold">{{ stats.generated_passwords_count || 0 }}</h3>
          <span class="text-[11px] text-zinc-500 font-medium">Entropy level: High</span>
        </div>
      </div>
    </div>

    <!-- Recent Secrets Activity -->
    <div class="space-y-6">
      <div class="flex items-center justify-between">
         <h4 class="text-sm font-semibold text-zinc-400 font-mono uppercase tracking-widest">Recent Activity</h4>
         <router-link to="/dashboard/logs" class="text-[12px] font-medium text-zinc-600 hover:text-white transition-colors">View all</router-link>
      </div>

      <div class="grid grid-cols-1 gap-3">
        <SecretListItem 
          v-for="secret in recentSecrets" 
          :key="secret.id" 
          :secret="secret" 
        />
      </div>
        
        <div v-if="secretStore.secrets.length === 0" class="py-12 border border-zinc-900 border-dashed rounded-2xl flex flex-col items-center justify-center text-zinc-600">
           <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2 opacity-50"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
           <span class="text-[13px]">No secrets archived yet.</span>
        </div>
    </div>

    <!-- Modals -->
    <VaultModal 
      :is-open="isVaultModalOpen" 
      @close="isVaultModalOpen = false" 
    />
    <SecretModal 
      :is-open="isSecretModalOpen" 
      @close="isSecretModalOpen = false" 
    />
  </div>
</template>
