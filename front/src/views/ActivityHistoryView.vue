<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useActivityStore } from '../stores/activity'
import Pagination from '../components/Pagination.vue'

const activityStore = useActivityStore()

onMounted(() => {
    activityStore.fetchLogs()
})

// Native date formatting — no date-fns needed
const formatTime = (dateStr: string) => {
    return new Date(dateStr).toLocaleTimeString('fr-FR', {
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    })
}

const formatGroupDate = (dateStr: string) => {
    const date = new Date(dateStr)
    const today = new Date()
    const yesterday = new Date()
    yesterday.setDate(today.getDate() - 1)

    const toDay = (d: Date) => d.toISOString().slice(0, 10)
    if (toDay(date) === toDay(today)) return "Aujourd'hui"
    if (toDay(date) === toDay(yesterday)) return "Hier"
    return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

const groupKey = (dateStr: string) => new Date(dateStr).toISOString().slice(0, 10)

const groupedLogs = computed(() => {
    const groups: Record<string, any[]> = {}
    activityStore.logs.forEach(log => {
        const date = groupKey(log.created_at)
        if (!groups[date]) groups[date] = []
        groups[date].push(log)
    })
    return groups
})

const getEventIcon = (type: string) => {
    if (type.includes('login')) return '🔑'
    if (type.includes('vault')) return '📦'
    if (type.includes('secret')) return '🔒'
    if (type.includes('master_key')) return '🛡️'
    return '📝'
}

const getEventLabel = (type: string) => {
    const labels: Record<string, string> = {
        'user_login': 'Connexion réussie',
        'user_registration': 'Création de compte',
        'vault_created': 'Coffre créé',
        'vault_updated': 'Coffre modifié',
        'vault_deleted': 'Coffre supprimé',
        'secret_created': 'Secret ajouté',
        'secret_revealed': 'Secret révélé',
        'secret_deleted': 'Secret supprimé',
        'master_key_generated': 'Clé Master générée',
        'master_key_unlocked': 'Coffre déverrouillé'
    }
    return labels[type] || type
}
</script>

<template>
    <div class="space-y-8 pb-12">
        <!-- Header -->
        <div class="flex items-center p-4 justify-between">
            <div class="space-y-1">
                <h2 class="text-3xl font-bold tracking-tight text-white">Journal d'Activité</h2>
                <p class="text-zinc-500">Historique complet des actions et événements de sécurité.</p>
            </div>
            
            <div class="flex items-center space-x-3">
                <button @click="activityStore.fetchLogs()" class="p-2 bg-zinc-900 border border-zinc-800 rounded-lg text-zinc-400 hover:text-emerald-400 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M3 21v-5h5"/></svg>
                </button>
            </div>
        </div>

        <div v-if="activityStore.loading && activityStore.logs.length === 0" class="flex flex-col items-center justify-center py-20 space-y-4">
            <div class="w-12 h-12 border-2 border-emerald-500/20 border-t-emerald-500 rounded-full animate-spin"></div>
            <p class="text-zinc-500 font-mono text-sm animate-pulse">Chargement de la timeline...</p>
        </div>

        <div v-else-if="activityStore.logs.length === 0" class="card-resend !p-20 text-center space-y-4">
            <div class="w-16 h-16 bg-zinc-900 rounded-2xl flex items-center justify-center border border-zinc-800 mx-auto text-2xl">
                📭
            </div>
            <p class="text-zinc-400 font-medium">Aucune activité enregistrée pour le moment.</p>
        </div>

        <div v-else class="space-y-10 relative">
            <!-- Timeline vertical line -->
            <div class="absolute left-[19px] top-4 bottom-4 w-[2px] bg-gradient-to-b from-emerald-500/50 via-emerald-500/10 to-transparent"></div>

            <div v-for="(logs, date) in groupedLogs" :key="date" class="space-y-6">
                <h3 class="text-[12px] font-bold text-zinc-500 uppercase tracking-[0.2em] sticky top-0 bg-black/50 backdrop-blur-md py-2 z-10 flex items-center space-x-3">
                    <span class="w-10 h-[1px] bg-zinc-800"></span>
                    <span>{{ formatGroupDate(date) }}</span>
                </h3>

                <div class="space-y-6 pl-10">
                    <div v-for="log in logs" :key="log.id" class="group relative">
                        <!-- Dot on timeline -->
                        <div class="absolute -left-[35px] top-1.5 w-3 h-3 rounded-full bg-zinc-900 border-2 border-zinc-700 group-hover:border-emerald-500 transition-colors z-20"></div>
                        
                        <div class="card-resend !p-4 hover:bg-emerald-500/[0.02] transition-all group-hover:border-emerald-500/30">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-4">
                                    <div class="text-xl w-8 h-8 flex items-center justify-center bg-zinc-900 rounded-lg border border-zinc-800">
                                        {{ getEventIcon(log.event_type) }}
                                    </div>
                                    <div>
                                        <h4 class="text-[14px] font-bold text-white group-hover:text-emerald-400 transition-colors">
                                            {{ getEventLabel(log.event_type) }}
                                        </h4>
                                        <p class="text-[12px] text-zinc-500 font-mono">
                                            <span class="text-emerald-500/70">{{ formatTime(log.created_at) }}</span>
                                            <span v-if="log.metadata_json?.name" class="ml-2 opacity-60">• {{ log.metadata_json.name }}</span>
                                            <span v-if="log.metadata_json?.title" class="ml-2 opacity-60">• {{ log.metadata_json.title }}</span>
                                        </p>
                                    </div>
                                </div>
                                
                                <div class="flex flex-col items-end space-y-1">
                                    <span class="text-[10px] px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-500 font-bold uppercase tracking-wider">
                                        {{ log.status }}
                                    </span>
                                    <span v-if="log.resource_type" class="text-[9px] text-zinc-600 font-mono uppercase">
                                        ID: {{ log.resource_id?.slice(0, 8) }}...
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pagination Component -->
        <Pagination 
            :page="activityStore.page"
            :pages="activityStore.pages"
            :total="activityStore.total"
            :limit="activityStore.limit"
            :start-item="(activityStore.page - 1) * activityStore.limit + 1"
            :end-item="Math.min(activityStore.page * activityStore.limit, activityStore.total)"
            :loading="activityStore.loading"
            @page-change="activityStore.fetchLogs"
        />
    </div>
</template>

<style scoped>
.card-resend {
    background: rgba(10, 10, 10, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
}
</style>
