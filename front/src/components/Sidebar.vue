<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const isTeamOpen = ref(false)
const isUserOpen = ref(false)

const toggleTeam = (e: Event) => {
  e.stopPropagation()
  isTeamOpen.value = !isTeamOpen.value
  if (isTeamOpen.value) isUserOpen.value = false
}

const toggleUser = (e: Event) => {
  e.stopPropagation()
  isUserOpen.value = !isUserOpen.value
  if (isUserOpen.value) isTeamOpen.value = false
}

const closeDropdowns = () => {
  isTeamOpen.value = false
  isUserOpen.value = false
}

onMounted(() => {
  window.addEventListener('click', closeDropdowns)
})

onUnmounted(() => {
  window.removeEventListener('click', closeDropdowns)
})

const navItems = [
  { 
    name: 'Dashboard', 
    path: '/dashboard', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>`
  },
  { 
    name: 'Vaults', 
    path: '/dashboard/vaults', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`
  },
  { 
    name: 'Generator', 
    path: '/dashboard/generator', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>`
  },
  { 
    name: 'Logs', 
    path: '/dashboard/logs', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>`
  },
  { 
    name: 'Settings', 
    path: '/dashboard/settings', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>`
  },
]

const activePath = computed(() => route.path)
</script>

<template>
  <aside class="w-64 border-r border-border bg-black flex flex-col z-40 relative transition-all duration-300">
    <!-- Workspace Selector -->
    <div class="h-16 flex items-center px-4 relative">
      <div 
        @click="toggleTeam"
        class="flex items-center justify-between w-full hover:bg-zinc-900 p-2 rounded-lg cursor-pointer transition-colors group"
      >
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-lg bg-zinc-800 border border-white/5 flex items-center justify-center shadow-lg">
            <span class="text-white text-sm font-bold opacity-60">o</span>
          </div>
          <div class="flex flex-col">
            <span class="text-[13px] font-semibold text-white leading-tight">Personal</span>
          </div>
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-500 group-hover:text-white transition-colors"><path d="m7 15 5 5 5-5"/><path d="m7 9 5-5 5 5"/></svg>
      </div>

      <!-- Teams Dropdown -->
      <transition 
        enter-active-class="transition duration-100 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-75 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <div v-if="isTeamOpen" class="absolute top-14 left-4 right-4 bg-black border border-zinc-800 rounded-xl shadow-2xl z-50 p-1 divide-y divide-zinc-800">
          <div class="p-2">
            <span class="text-[11px] text-zinc-500 px-2 font-medium mb-1 block">Teams</span>
            <div class="flex items-center justify-between p-2 rounded-lg bg-zinc-900 text-white group cursor-pointer hover:bg-zinc-800 transition-colors">
              <div class="flex items-center space-x-3">
                 <div class="w-7 h-7 rounded-lg bg-zinc-800 border border-white/5 flex items-center justify-center">
                    <span class="text-[12px] opacity-60">o</span>
                 </div>
                 <span class="text-[13px] font-medium">Personal</span>
              </div>
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-white"><polyline points="20 6 9 17 4 12"/></svg>
            </div>
          </div>
          <div class="p-1">
             <button class="w-full flex items-center space-x-3 p-2 rounded-lg hover:bg-zinc-900 text-zinc-400 hover:text-white transition-colors text-[13px] font-medium">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
               <span>Create Team</span>
             </button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Master Key Input -->
    <div class="px-6 py-2">
       <div class="relative group">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-600 transition-colors group-focus-within:text-zinc-400"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3v-3z"/></svg>
          <div 
            v-if="authStore.publicToken && authStore.publicToken !== 'VAT-PENDING-SYNC'"
            class="w-full bg-zinc-900/30 border border-zinc-900/50 rounded-lg pl-8 pr-3 py-1.5 text-[10px] focus:outline-none transition-all placeholder:text-zinc-800 font-mono text-emerald-500/70 truncate flex items-center h-[30px]"
            title="Votre Vault est déverrouillé"
          >
            {{ authStore.publicToken }}
          </div>
          <button 
            v-else-if="authStore.publicToken === 'VAT-PENDING-SYNC' || (!authStore.masterKey && authStore.hasMasterKey)"
            @click="authStore.publicToken === 'VAT-PENDING-SYNC' ? $router.push('/setup-master-key') : $emit('request-unlock')"
            class="w-full bg-emerald-500/10 border border-emerald-500/20 hover:bg-emerald-500/20 rounded-lg pl-8 pr-3 py-1.5 text-[10px] text-emerald-500 font-medium transition-all flex items-center h-[30px] group/btn"
          >
            <span>{{ authStore.publicToken === 'VAT-PENDING-SYNC' ? 'Fix Token Sync' : 'Unlock Vault' }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="ml-auto opacity-0 group-hover/btn:opacity-100 transition-all"><path d="m9 18 6-6-6-6"/></svg>
          </button>
       </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 py-4 px-3 space-y-1">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center space-x-3 px-3 py-2 rounded-lg transition-standard group text-[13px]"
        :class="[
          activePath === item.path 
            ? 'bg-zinc-900 text-white shadow-sm' 
            : 'text-zinc-400 hover:text-white hover:bg-zinc-900/50'
        ]"
      >
        <div v-html="item.icon" class="opacity-70 group-hover:opacity-100 transition-opacity"></div>
        <span class="font-medium">{{ item.name }}</span>
      </router-link>
    </nav>

    <!-- Sidebar Footer / User Profile -->
    <div class="p-4 border-t border-border relative">
      <div 
        @click="toggleUser"
        class="flex items-center justify-between w-full hover:bg-zinc-900 p-2 rounded-lg cursor-pointer transition-colors group"
      >
        <div class="flex items-center space-x-3 overflow-hidden">
          <div class="w-8 h-8 rounded-full bg-zinc-800 border border-white/5 flex items-center justify-center shrink-0">
            <span class="text-zinc-400 text-[10px]">{{ authStore.userEmail?.charAt(0).toUpperCase() }}</span>
          </div>
          <div class="flex flex-col overflow-hidden">
            <span class="text-[12px] font-medium text-white truncate">{{ authStore.userEmail }}</span>
          </div>
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-500 shrink-0"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
      </div>

      <!-- User Dropdown -->
      <transition 
        enter-active-class="transition duration-100 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-75 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <div v-if="isUserOpen" class="absolute bottom-16 left-4 right-4 bg-black border border-zinc-800 rounded-xl shadow-2xl z-50 p-1 divide-y divide-zinc-800">
           <div class="p-1">
             <button class="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-900 text-zinc-400 hover:text-white transition-colors group">
               <div class="flex items-center space-x-3">
                 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="10" r="3"/><path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"/></svg>
                 <span class="text-[13px] font-medium">My profile</span>
               </div>
             </button>
             <button class="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-900 text-zinc-400 hover:text-white transition-colors group">
               <div class="flex items-center space-x-3">
                 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
                 <span class="text-[13px] font-medium">Toggle theme</span>
               </div>
               <span class="text-[11px] font-bold text-zinc-700 bg-zinc-900 px-1.5 py-0.5 rounded border border-white/5">M</span>
             </button>
           </div>
           <div class="p-1">
              <button class="w-full flex items-center space-x-3 p-2 rounded-lg hover:bg-zinc-900 text-zinc-400 hover:text-white transition-colors text-[13px] font-medium">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
               <span>Homepage</span>
             </button>
             <button class="w-full flex items-center space-x-3 p-2 rounded-lg hover:bg-zinc-900 text-zinc-400 hover:text-white transition-colors text-[13px] font-medium">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
               <span>Onboarding</span>
             </button>
           </div>
           <div class="p-1">
              <button 
                @click="authStore.logout(); closeDropdowns()" 
                class="w-full flex items-center space-x-3 p-2 rounded-lg hover:bg-zinc-900 text-zinc-400 hover:text-white transition-colors text-[13px] font-medium"
              >
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
               <span>Log out</span>
              </button>
           </div>
        </div>
      </transition>
    </div>
  </aside>
</template>
