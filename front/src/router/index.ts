import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/dashboard',
            component: () => import('../layouts/DashboardLayout.vue'),
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    name: 'dashboard',
                    component: () => import('../views/DashboardHome.vue')
                },
                {
                    path: 'vaults',
                    name: 'vaults',
                    component: () => import('../views/VaultsView.vue')
                },
                {
                    path: 'generator',
                    name: 'generator',
                    component: () => import('../views/DashboardHome.vue')
                },
                {
                    path: 'logs',
                    name: 'logs',
                    component: () => import('../views/DashboardHome.vue')
                },
                {
                    path: 'settings',
                    name: 'settings',
                    component: () => import('../views/DashboardHome.vue')
                }
            ]
        },
        {
            path: '/',
            redirect: '/login'
        }
    ]
})

router.beforeEach((to) => {
    const authStore = useAuthStore()
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        return '/login'
    }
})

export default router
