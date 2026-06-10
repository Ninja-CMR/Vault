<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const userEmail = computed(() => authStore.userEmail || 'Non connecté')
const masterKeyStatus = computed(() => authStore.hasMasterKey ? 'Configurée' : 'Non configurée')

const documentationLink = 'https://docs.vault-app.com' // Placeholder
const supportNumber = '+237 696 172 899'

const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    // On pourrait ajouter un toast ici
}
</script>

<template>
    <div class="p-8 space-y-12 max-w-7xl mx-auto pb-20">
        <!-- Header -->
        <div class="flex flex-col space-y-2">
            <h2 class="text-3xl font-bold tracking-tight text-white">Paramètres</h2>
            <p class="text-zinc-500 text-sm">Gérez votre compte et accédez au support.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Main Settings (Left/Center) -->
            <div class="lg:col-span-2 space-y-8">
                <!-- Profile Section -->
                <section class="space-y-4">
                    <h3 class="text-[12px] font-bold text-zinc-500 uppercase tracking-widest flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                        <span>Profil Utilisateur</span>
                    </h3>
                    <div class="card-resend p-6 space-y-6">
                        <div class="flex items-center justify-between">
                            <div class="flex flex-col space-y-1">
                                <span class="text-xs text-zinc-500">Adresse Email</span>
                                <span class="text-white font-medium">{{ userEmail }}</span>
                            </div>
                            <span class="px-2 py-1 bg-emerald-500/10 text-emerald-500 text-[10px] font-bold rounded border border-emerald-500/20">VÉRIFIÉ</span>
                        </div>
                        <div class="pt-6 border-t border-zinc-800/50 flex items-center justify-between">
                            <div class="flex flex-col space-y-1">
                                <span class="text-xs text-zinc-500">Statut du Compte</span>
                                <span class="text-white font-medium">Actif</span>
                            </div>
                            <button class="text-xs text-zinc-400 hover:text-white transition-colors">Modifier le mot de passe</button>
                        </div>
                    </div>
                </section>

                <!-- Security Section -->
                <section class="space-y-4">
                    <h3 class="text-[12px] font-bold text-zinc-500 uppercase tracking-widest flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        <span>Sécurité & Chiffrement</span>
                    </h3>
                    <div class="card-resend p-6 space-y-6">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <div class="w-10 h-10 bg-zinc-900 border border-zinc-800 rounded-xl flex items-center justify-center text-xl">
                                    🛡️
                                </div>
                                <div class="flex flex-col">
                                    <span class="text-white font-medium">Clé Maîtresse (Master Key)</span>
                                    <span class="text-xs text-zinc-500">{{ masterKeyStatus }}</span>
                                </div>
                            </div>
                            <router-link to="/setup-master-key" class="button-secondary !py-1.5 !px-4 text-[11px]">Gérer</router-link>
                        </div>
                        <div class="pt-6 border-t border-zinc-800/50">
                            <div class="flex items-center justify-between opacity-50 cursor-not-allowed">
                                <div class="flex items-center space-x-4">
                                    <div class="w-10 h-10 bg-zinc-900 border border-zinc-800 rounded-xl flex items-center justify-center text-xl">
                                        📱
                                    </div>
                                    <div class="flex flex-col">
                                        <span class="text-white font-medium">Authentification à deux facteurs (2FA)</span>
                                        <span class="text-xs text-zinc-500 italic">Bientôt disponible</span>
                                    </div>
                                </div>
                                <span class="text-xs text-zinc-600">Désactivé</span>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Documentation & Resources -->
                <section class="space-y-4">
                    <h3 class="text-[12px] font-bold text-zinc-500 uppercase tracking-widest flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M8 7h6"/><path d="M8 11h8"/></svg>
                        <span>Aide & Documentation</span>
                    </h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <a :href="documentationLink" target="_blank" class="card-resend p-4 hover:bg-white/[0.02] transition-all group border-emerald-500/10 active:scale-[0.98]">
                            <div class="flex items-center justify-between mb-2">
                                <span class="p-2 bg-zinc-900 border border-zinc-800 rounded-lg group-hover:border-emerald-500/50 transition-colors">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                                </span>
                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-600 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg>
                            </div>
                            <h4 class="text-sm font-bold text-white">Documentation API</h4>
                            <p class="text-[11px] text-zinc-500 mt-1">Guide complet pour l'intégration de Vault.</p>
                        </a>
                        <div class="card-resend p-4 hover:bg-white/[0.02] transition-all group border-emerald-500/10">
                            <div class="flex items-center justify-between mb-2">
                                <span class="p-2 bg-zinc-900 border border-zinc-800 rounded-lg">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>
                                </span>
                            </div>
                            <h4 class="text-sm font-bold text-white">FAQs</h4>
                            <p class="text-[11px] text-zinc-500 mt-1">Réponses aux questions les plus fréquentes.</p>
                        </div>
                    </div>
                </section>
            </div>

            <!-- Support Sidebar (Right) -->
            <div class="space-y-8">
                <section class="space-y-4">
                    <h3 class="text-[12px] font-bold text-zinc-500 uppercase tracking-widest flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l2.27-2.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                        <span>Support Client</span>
                    </h3>
                    <div class="relative overflow-hidden group">
                        <!-- Decorative background -->
                        <div class="absolute inset-0 bg-gradient-to-br from-emerald-500/20 via-transparent to-transparent opacity-50 group-hover:opacity-70 transition-opacity"></div>
                        
                        <div class="relative card-resend p-6 border-emerald-500/20 space-y-6">
                            <div class="space-y-2">
                                <h4 class="text-lg font-bold text-white">Besoin d'aide ?</h4>
                                <p class="text-sm text-zinc-400">Notre équipe technique est disponible au Cameroun pour vous accompagner.</p>
                            </div>
                            
                            <div class="flex flex-col space-y-3">
                                <a :href="'tel:' + supportNumber.replace(/\s/g, '')" class="flex items-center justify-between p-3 bg-black/40 border border-zinc-800 rounded-xl group/item hover:border-emerald-500/50 transition-all">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-500">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l2.27-2.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                                        </div>
                                        <span class="text-sm font-mono text-white">{{ supportNumber }}</span>
                                    </div>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-600 group-hover/item:text-emerald-500 transition-colors"><path d="m9 18 6-6-6-6"/></svg>
                                </a>
                                <button @click="copyToClipboard(supportNumber)" class="w-full py-2.5 text-[11px] font-bold text-zinc-500 hover:text-white transition-colors uppercase tracking-widest">
                                    Copier le numéro
                                </button>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Project Info -->
                <section class="card-resend p-6 border-zinc-900 bg-zinc-900/10">
                    <div class="text-[10px] text-zinc-700 font-mono">
                        © 2026 Vault Technologies. Tous droits réservés.
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<style scoped>
.card-resend {
    background: rgba(10, 10, 10, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    backdrop-filter: blur(10px);
}

.button-primary {
    background: white;
    color: black;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.button-primary:hover {
    background: rgba(255, 255, 255, 0.9);
    transform: translateY(-1px);
}

.button-secondary {
    background: rgba(255, 255, 255, 0.05);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-weight: 500;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.button-secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
}
</style>
