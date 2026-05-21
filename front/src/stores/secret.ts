import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'
import { encryptData, decryptData } from '../utils/encryption'

export interface Secret {
    id: string
    vault_id: string
    title: string
    type: 'LOGIN' | 'API_KEY' | 'TOKEN' | 'NOTE'
    description?: string
    created_at: string
    encrypted_value?: string
}

export const useSecretStore = defineStore('secret', {
    state: () => ({
        secrets: [] as Secret[],
        loading: false,
        error: null as string | null
    }),

    actions: {
        async fetchSecretsByVaultId(vaultId: string) {
            this.loading = true
            this.error = null
            try {
                const authStore = useAuthStore()
                const response = await axios.get(`http://localhost:8000/secrets/vaults/${vaultId}`, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })
                return response.data
            } catch (err: any) {
                this.error = 'Failed to fetch vault secrets'
                throw err
            } finally {
                this.loading = false
            }
        },

        async fetchAllSecrets() {
            this.loading = true
            this.error = null
            try {
                const authStore = useAuthStore()
                console.log('Fetching all secrets...')
                const response = await axios.get('http://localhost:8000/secrets/all', {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })
                console.log('Secrets fetched successfully:', response.data.length)
                this.secrets = response.data
            } catch (err: any) {
                console.error('Failed to fetch secrets:', err)
                this.error = 'Failed to fetch all secrets'
            } finally {
                this.loading = false
            }
        },

        async createSecret(vault_id: string, title: string, type: string, rawValue: any, description?: string) {
            const authStore = useAuthStore()
            if (!authStore.masterKey) throw new Error('Master key not set')

            this.loading = true
            try {
                // Encrypt the JSON value
                const jsonValue = JSON.stringify(rawValue)
                const encryptedValue = await encryptData(jsonValue, authStore.masterKey, authStore.userEmail || 'static-salt')

                const response = await axios.post(`http://localhost:8000/secrets/vaults/${vault_id}`, {
                    title,
                    type,
                    encrypted_value: encryptedValue,
                    description
                }, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })

                this.secrets.unshift(response.data)
                return response.data
            } catch (err: any) {
                this.error = err.response?.data?.detail || 'Failed to create secret'
                throw err
            } finally {
                this.loading = false
            }
        },

        async revealSecret(secretId: string) {
            const authStore = useAuthStore()
            if (!authStore.masterKey) throw new Error('Master key not set')

            try {
                const response = await axios.get(`http://localhost:8000/secrets/${secretId}/reveal`, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })

                const encryptedValue = response.data.encrypted_value
                const decryptedJson = await decryptData(encryptedValue, authStore.masterKey, authStore.userEmail || 'static-salt')

                return JSON.parse(decryptedJson)
            } catch (err: any) {
                throw new Error('Failed to reveal secret')
            }
        }
    }
})
