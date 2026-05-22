<script setup lang="ts">
defineProps<{
    page: number
    pages: number
    total: number
    limit: number
    startItem: number
    endItem: number
    loading: boolean
}>()

const emit = defineEmits<{
    (e: 'page-change', page: number): void
}>()
</script>

<template>
    <div v-if="pages > 0" class="flex items-center justify-between px-4 py-8 border-t border-zinc-800/50">
        <div class="text-sm text-zinc-500 font-mono">
            Page <span class="text-emerald-500">{{ page }}</span> sur <span class="text-white">{{ pages }}</span>
            <span class="ml-2 opacity-50">• {{ total }} éléments</span>
        </div>

        <div class="flex items-center space-x-2">
            <button 
                @click="emit('page-change', page - 1)" 
                :disabled="page === 1 || loading"
                class="px-4 py-2 bg-zinc-900 border border-zinc-800 rounded-lg text-sm font-medium text-zinc-400 hover:text-emerald-400 hover:border-emerald-500/30 disabled:opacity-50 disabled:hover:text-zinc-400 disabled:hover:border-zinc-800 transition-all flex items-center space-x-2"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                <span>Précédent</span>
            </button>

            <div class="flex items-center px-4 space-x-1">
                <span class="text-sm font-mono text-emerald-500">{{ page }}</span>
                <span class="text-sm font-mono text-zinc-600">/</span>
                <span class="text-sm font-mono text-zinc-400">{{ pages }}</span>
            </div>

            <button 
                @click="emit('page-change', page + 1)" 
                :disabled="page === pages || loading"
                class="px-4 py-2 bg-zinc-900 border border-zinc-800 rounded-lg text-sm font-medium text-zinc-400 hover:text-emerald-400 hover:border-emerald-500/30 disabled:opacity-50 disabled:hover:text-zinc-400 disabled:hover:border-zinc-800 transition-all flex items-center space-x-2"
            >
                <span>Suivant</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
            </button>
        </div>
    </div>
</template>
