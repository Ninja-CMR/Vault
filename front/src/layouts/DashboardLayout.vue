<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Sidebar from '../components/Sidebar.vue'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-black flex text-white font-sans">
    <!-- Sidebar -->
    <Sidebar @logout="logout" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- Header / Top Bar -->
      <header class="h-16 border-b border-border flex items-center justify-between px-8 bg-black/50 backdrop-blur-xl z-30">
        <div class="flex items-center space-x-2 text-[13px] font-medium text-zinc-400">
          <span class="hover:text-white cursor-pointer transition-colors">Vault</span>
          <span class="text-zinc-600">/</span>
          <span class="text-white">Overview</span>
        </div>
        
        <div class="flex items-center space-x-4">
          <a href="#" class="text-[13px] text-zinc-400 hover:text-white transition-colors">Docs</a>
          <button class="bg-zinc-800 hover:bg-zinc-700 text-white text-[13px] px-3 py-1.5 rounded-lg border border-white/5 transition-standard">
            Need help?
          </button>
          <div class="h-4 w-px bg-zinc-800"></div>
          <button 
            @click="logout"
            class="text-[13px] text-zinc-400 hover:text-white transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 overflow-y-auto relative">
        <router-view v-slot="{ Component }">
          <transition 
            name="fade" 
            mode="out-in"
          >
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
