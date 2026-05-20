<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useDashboard } from '../composables/useDashboard'
import { useVaultStore } from '../stores/vault'
import { formatDate } from '../utils/format'
import VaultModal from '../components/modals/VaultModal.vue'

const { vaults, fetchDashboardData, isLoading } = useDashboard()
const vaultStore = useVaultStore()
const isVaultModalOpen = ref(false)
const searchQuery = ref('')

onMounted(async () => {
  await fetchDashboardData()
})

const filteredVaults = ref(vaults) // Simplified for now, can add reactive filter later
</script>

<template>
  <div class="h-full overflow-y-auto p-8 space-y-10 custom-scrollbar">
    <div class="flex items-center justify-between">
      <div class="space-y-1">
        <h1 class="text-3xl font-bold tracking-tight text-white">Your Vaults</h1>
        <p class="text-zinc-500 text-sm">Manage and organize your secure containers.</p>
      </div>
      
      <button 
        @click="isVaultModalOpen = true"
        class="button-primary flex items-center space-x-2 px-6 py-2.5"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
        <span>New Vault</span>
      </button>
    </div>

    <!-- Search/Filter (Optional Addition) -->
    <div v-if="vaults.length > 0" class="relative max-w-md">
       <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
       <input 
         v-model="searchQuery"
         type="text" 
         placeholder="Search vaults..." 
         class="input-resend w-full pl-10 h-10"
       />
    </div>

    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
      <div v-for="i in 6" :key="i" class="h-48 bg-zinc-900/50 rounded-2xl border border-zinc-900"></div>
    </div>

    <div v-else-if="vaults.length === 0" class="flex flex-col items-center justify-center py-20 border border-dashed border-zinc-900 rounded-3xl space-y-4">
      <div class="w-16 h-16 bg-zinc-950 rounded-full flex items-center justify-center border border-zinc-900 text-zinc-700">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      </div>
      <div class="text-center">
        <h3 class="text-white">No vaults found</h3>
        <p class="text-zinc-500 text-sm max-w-xs mx-auto mt-2">Get started by creating your first secure container to store your secrets.</p>
      </div>
      <button @click="isVaultModalOpen = true" class="button-primary text-sm mt-4">Create First Vault</button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div 
        v-for="vault in vaults" 
        :key="vault.id"
        class="card-resend flex flex-col justify-between group cursor-pointer border-transparent hover:border-zinc-800 transition-all duration-300"
      >
         <div class="space-y-4">
           <div class="flex items-center justify-between">
             <div class="w-10 h-10 bg-zinc-900 rounded-xl flex items-center justify-center border border-zinc-800 transition-colors group-hover:border-zinc-700">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-400 group-hover:text-white transition-colors"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
             </div>
             <button class="p-1.5 text-zinc-600 hover:text-white transition-colors">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
             </button>
           </div>
           
           <div>
             <h3 class="text-lg font-bold text-white uppercase tracking-tight group-hover:text-primary transition-colors">{{ vault.name }}</h3>
             <p class="text-zinc-500 text-[13px] line-clamp-2 mt-1">{{ vault.description || 'No description provided' }}</p>
           </div>
         </div>

         <div class="pt-6 mt-6 border-t border-zinc-900/50 flex items-center justify-between">
           <span class="text-[11px] font-medium text-zinc-600 uppercase tracking-widest">{{ formatDate(vault.created_at) }}</span>
           <router-link :to="`/vaults/${vault.id}`" class="text-[12px] font-bold text-white flex items-center space-x-1 hover:translate-x-1 transition-transform">
             <span>Explore</span>
             <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
           </router-link>
         </div>
      </div>
    </div>

    <!-- Modals -->
    <VaultModal 
      :is-open="isVaultModalOpen" 
      @close="isVaultModalOpen = false" 
    />
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #18181b;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #27272a;
}
</style>
