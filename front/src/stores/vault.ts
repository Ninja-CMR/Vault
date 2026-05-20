import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export interface Vault {
    id: string
    name: string
    description?: string
    created_at: string
}

export const useVaultStore = defineStore('vault', {
    state: () => ({
        vaults: [] as Vault[],
        loading: false,
        error: null as string | null,
    }),

    actions: {
        async fetchVaults() {
            this.loading = true
            this.error = null
            try {
                const authStore = useAuthStore()
                const response = await axios.get('http://localhost:8000/vaults', {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })
                this.vaults = response.data
            } catch (err: any) {
                this.error = err.response?.data?.detail || 'Failed to fetch vaults'
            } finally {
                this.loading = false
            }
        },

        async createVault(name: string, description?: string) {
            this.loading = true
            this.error = null
            try {
                const authStore = useAuthStore()
                const response = await axios.post('http://localhost:8000/vaults', {
                    name,
                    description
                }, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })
                this.vaults.push(response.data)
                return response.data
            } catch (err: any) {
                this.error = err.response?.data?.detail || 'Failed to create vault'
                throw err
            } finally {
                this.loading = false
            }
        },

        async deleteVault(vaultId: string) {
            try {
                const authStore = useAuthStore()
                await axios.delete(`http://localhost:8000/vaults/${vaultId}`, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })
                this.vaults = this.vaults.filter(v => v.id !== vaultId)
            } catch (err: any) {
                this.error = err.response?.data?.detail || 'Failed to delete vault'
                throw err
            }
        }
    }
})
