<script setup lang="ts">
import { Form } from 'vee-validate'
import * as yup from 'yup'
import BaseInput from '../components/BaseInput.vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const schema = yup.object({
  email: yup.string().required('Email requis').email('Format invalide'),
  password: yup.string().required('Mot de passe requis')
})

const onSubmit = async (values: any) => {
  try {
    const response = await axios.post('http://localhost:8000/auth/login', {
      email: values.email,
      password: values.password
    })
    
    const { access_token } = response.data
    authStore.setSession(values.email, access_token)
    
    // Redirection vers le dashboard (qui sera fait plus tard)
    router.push('/dashboard')
  } catch (error: any) {
    console.error('Erreur connexion:', error.response?.data?.detail || error.message)
    alert(error.response?.data?.detail || "Échec de l'authentification")
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-6 bg-black">
    <div class="w-full max-w-[400px] space-y-8">
      <!-- Logo / Header -->
      <div class="flex flex-col items-center space-y-6">
        <div class="w-14 h-14 bg-gradient-to-b from-zinc-700 to-zinc-950 rounded-2xl flex items-center justify-center border border-zinc-600 shadow-[0_10px_30px_rgba(0,0,0,0.5)]">
            <span class="text-white font-bold text-2xl opacity-60">o</span>
        </div>
        <div class="text-center space-y-1">
          <h1 class="text-3xl font-bold tracking-tight text-white">Log in to Vault</h1>
          <p class="text-zinc-500 text-[15px]">
            Don't have an account? 
            <router-link to="/register" class="text-white hover:underline">Sign up</router-link>
          </p>
        </div>
      </div>

      <div class="card-resend !p-8">
        <Form @submit="onSubmit" :validation-schema="schema" class="space-y-4">
          <BaseInput
            name="email"
            label="Email"
            type="email"
            placeholder="alan.turing@example.com"
          />
          
          <BaseInput
            name="password"
            label="Password"
            type="password"
            placeholder="••••••••"
          />

          <div class="pt-2">
            <button type="submit" class="button-primary w-full py-2.5">
              Log In
            </button>
          </div>
        </Form>
      </div>

      <div class="text-center">
        <a href="#" class="text-zinc-500 hover:text-white text-xs transition-colors">Forgot your password?</a>
      </div>
    </div>
  </div>
</template>
