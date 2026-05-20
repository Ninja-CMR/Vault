import { defineStore } from 'pinia'

interface UserState {
    userEmail: string | null
    token: string | null
    isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
    state: (): UserState => ({
        userEmail: localStorage.getItem('vault_user_email'),
        token: localStorage.getItem('vault_token'),
        isAuthenticated: !!localStorage.getItem('vault_token')
    }),
    actions: {
        setSession(email: string, token: string) {
            this.userEmail = email
            this.token = token
            this.isAuthenticated = true
            localStorage.setItem('vault_user_email', email)
            localStorage.setItem('vault_token', token)
        },
        logout() {
            this.userEmail = null
            this.token = null
            this.isAuthenticated = false
            localStorage.removeItem('vault_user_email')
            localStorage.removeItem('vault_token')
        }
    }
})
