<script setup lang="ts">
import { Form } from 'vee-validate'
import * as yup from 'yup'
import BaseInput from '../components/BaseInput.vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
const router = useRouter()

const schema = yup.object({
  username: yup.string().required('Username is required').min(3, 'At least 3 characters'),
  email: yup.string().required('Email is required').email('Invalid email format'),
  password: yup.string()
    .required('Password is required')
    .min(8, 'Minimum 8 characters')
    .matches(/[A-Z]/, 'Must contain an uppercase letter')
    .matches(/[a-z]/, 'Must contain a lowercase letter')
    .matches(/\d/, 'Must contain a number')
    .matches(/[!@#$%^&*(),.?":{}|<>]/, 'Must contain a special character'),
  confirmPassword: yup.string()
    .required('Confirmation is required')
    .oneOf([yup.ref('password')], 'Passwords do not match')
})

const onSubmit = async (values: any) => {
  try {
    // Appel API backend (back/app/routes/auth.py)
    await axios.post('http://localhost:8000/auth/register', {
      username: values.username,
      email: values.email,
      password: values.password
    })
    
    // Après inscription, on redirige vers le login
    router.push('/login')
  } catch (error: any) {
    console.error('Erreur inscription:', error.response?.data?.detail || error.message)
    alert(error.response?.data?.detail || "An error occurred during registration")
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
          <h1 class="text-3xl font-bold tracking-tight text-white">Create an account</h1>
          <p class="text-zinc-500 text-[15px]">
            Already have an account? 
            <router-link to="/login" class="text-white hover:underline">Log in</router-link>
          </p>
        </div>
      </div>

      <div class="card-resend !p-8">
        <Form @submit="onSubmit" :validation-schema="schema" class="space-y-4">
          <BaseInput
            name="username"
            label="Username"
            placeholder="johndoe"
          />

          <BaseInput
            name="email"
            label="Email"
            type="email"
            placeholder="john@example.com"
          />
          
          <BaseInput
            name="password"
            label="Password"
            type="password"
            placeholder="••••••••"
          />

          <BaseInput
            name="confirmPassword"
            label="Confirm Password"
            type="password"
            placeholder="••••••••"
          />

          <div class="pt-2">
            <button type="submit" class="button-primary w-full py-2.5">
              Create Account
            </button>
          </div>
        </Form>
      </div>

      <p class="text-center text-zinc-500 text-[11px] leading-relaxed">
        By signing up, you agree to our <a href="#" class="underline hover:text-white">Terms of Service</a> and <a href="#" class="underline hover:text-white">Privacy Policy</a>.
      </p>
    </div>
  </div>
</template>
