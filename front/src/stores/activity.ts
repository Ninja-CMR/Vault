import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export interface ActivityLog {
    id: string
    event_type: string
    resource_type: string | null
    resource_id: string | null
    status: string
    created_at: string
    metadata_json: any | null
}

export const useActivityStore = defineStore('activity', {
    state: () => ({
        logs: [] as ActivityLog[],
        total: 0,
        page: 1,
        limit: 20,
        pages: 0,
        loading: false,
        error: null as string | null
    }),
    actions: {
        async fetchLogs(page: number = 1, limit: number = 20) {
            this.loading = true
            this.error = null
            try {
                const authStore = useAuthStore()
                const response = await axios.get('http://localhost:8000/activity/logs', {
                    params: { page, limit },
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })

                this.logs = response.data.items
                this.total = response.data.total
                this.page = response.data.page
                this.limit = response.data.limit
                this.pages = response.data.pages
            } catch (err: any) {
                this.error = 'Failed to fetch activity logs'
                console.error(err)
            } finally {
                this.loading = false
            }
        }
    }
})
