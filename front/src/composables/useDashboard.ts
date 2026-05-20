import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

export interface Vault {
    id: string
    name: string
    description?: string
    created_at: string
}

export interface Stats {
    vaults_count: number
    secrets_count: number
    generated_passwords_count: number
}

const stats = ref<Stats>({
    vaults_count: 0,
    secrets_count: 0,
    generated_passwords_count: 0
})
const vaults = ref<Vault[]>([])
const isLoading = ref(true)

export function useDashboard() {
    const authStore = useAuthStore()

    const fetchDashboardData = async () => {
        isLoading.value = true
        try {
            const [statsRes, vaultsRes] = await Promise.all([
                axios.get('http://localhost:8000/tools/stats', {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                }),
                axios.get('http://localhost:8000/vaults', {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })
            ])
            stats.value = statsRes.data
            vaults.value = vaultsRes.data
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error)
        } finally {
            isLoading.value = false
        }
    }

    return {
        stats,
        vaults,
        isLoading,
        fetchDashboardData
    }
}
