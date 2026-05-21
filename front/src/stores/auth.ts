import { defineStore } from 'pinia'

interface UserState {
    userEmail: string | null
    token: string | null
    isAuthenticated: boolean
    hasMasterKey: boolean
    masterKey: string | null
    publicToken: string | null
}

export const useAuthStore = defineStore('auth', {
    state: (): UserState => ({
        userEmail: localStorage.getItem('vault_user_email'),
        token: localStorage.getItem('vault_token'),
        isAuthenticated: !!localStorage.getItem('vault_token'),
        hasMasterKey: localStorage.getItem('vault_has_master_key') === 'true',
        masterKey: null,
        publicToken: null
    }),
    actions: {
        setSession(email: string, token: string) {
            this.userEmail = email
            this.token = token
            this.isAuthenticated = true
            localStorage.setItem('vault_user_email', email)
            localStorage.setItem('vault_token', token)
        },
        setMasterKey(key: string | null, token: string | null = null) {
            this.masterKey = key
            if (token) this.publicToken = token
        },
        async checkMasterKeyStatus() {
            if (!this.token) return
            try {
                const response = await fetch('http://localhost:8000/security/master-key/status', {
                    headers: { 'Authorization': `Bearer ${this.token}` }
                })
                const data = await response.json()
                this.hasMasterKey = data.has_master_key
                this.publicToken = data.public_token
                localStorage.setItem('vault_has_master_key', String(data.has_master_key))
            } catch (error) {
                console.error('Failed to check master key status:', error)
            }
        },
        async unlockMasterKey(password: string) {
            if (!this.token) return
            try {
                const response = await fetch('http://localhost:8000/security/master-key/unlock', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ password })
                })
                const data = await response.json()
                if (response.ok) {
                    this.masterKey = data.master_key
                    this.publicToken = data.public_token
                    return true
                } else {
                    throw new Error(data.detail || 'Failed to unlock')
                }
            } catch (error) {
                console.error('Failed to unlock master key:', error)
                throw error
            }
        },
        logout() {
            this.userEmail = null
            this.token = null
            this.isAuthenticated = false
            this.hasMasterKey = false
            localStorage.removeItem('vault_user_email')
            localStorage.removeItem('vault_token')
            localStorage.removeItem('vault_has_master_key')
        }
    }
})
