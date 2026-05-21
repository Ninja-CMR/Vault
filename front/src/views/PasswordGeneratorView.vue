<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

// ── State ────────────────────────────────────────────────────
const length = ref(16)
const includeUppercase = ref(true)
const includeLowercase = ref(true)
const includeNumbers = ref(true)
const includeSymbols = ref(false)

const generatedPassword = ref('')
const strength = ref('')
const entropyScore = ref(0)
const isGenerating = ref(false)
const isCopied = ref(false)
const showPassword = ref(true)
const error = ref('')

// ── Options ───────────────────────────────────────────────────
const options = [
  { label: 'Uppercase letters', example: 'A–Z', model: includeUppercase },
  { label: 'Lowercase letters', example: 'a–z', model: includeLowercase },
  { label: 'Numbers',           example: '0–9', model: includeNumbers },
  { label: 'Symbols',           example: '!@#$', model: includeSymbols },
]

// ── Computed ──────────────────────────────────────────────────
const atLeastOneSelected = computed(() =>
  includeUppercase.value || includeLowercase.value || includeNumbers.value || includeSymbols.value
)

const strengthColor = computed(() => {
  if (entropyScore.value < 40) return '#ef4444'
  if (entropyScore.value < 60) return '#f97316'
  if (entropyScore.value < 80) return '#eab308'
  return '#10b981'
})

const strengthPercent = computed(() =>
  Math.min(100, Math.round((entropyScore.value / 120) * 100))
)

const strengthLabel = computed(() => {
  if (entropyScore.value < 40) return 'Weak'
  if (entropyScore.value < 60) return 'Moderate'
  if (entropyScore.value < 80) return 'Strong'
  return 'Very Strong'
})

const displayedPassword = computed(() =>
  showPassword.value
    ? generatedPassword.value
    : '•'.repeat(generatedPassword.value.length)
)

// ── Methods ───────────────────────────────────────────────────
const generate = async () => {
  if (!atLeastOneSelected.value) {
    error.value = 'Select at least one character type.'
    return
  }
  error.value = ''
  isGenerating.value = true
  isCopied.value = false

  try {
    const { data } = await axios.post(
      'http://localhost:8000/tools/password-generator',
      {
        length: length.value,
        include_uppercase: includeUppercase.value,
        include_lowercase: includeLowercase.value,
        include_numbers: includeNumbers.value,
        include_symbols: includeSymbols.value,
      },
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    )
    generatedPassword.value = data.password
    strength.value = data.strength
    entropyScore.value = data.entropy_score
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Generation failed.'
  } finally {
    isGenerating.value = false
  }
}

const copyPassword = async () => {
  if (!generatedPassword.value) return
  await navigator.clipboard.writeText(generatedPassword.value)
  isCopied.value = true
  setTimeout(() => (isCopied.value = false), 2000)
}

onMounted(() => generate())
</script>

<template>
  <div class="h-full overflow-y-auto p-8 space-y-8 max-w-5xl mx-auto custom-scrollbar">

    <!-- Header -->
    <div class="space-y-1">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-400">
            <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-white">Password Generator</h1>
          <p class="text-zinc-500 text-[13px]">Cryptographically secure. Never stored.</p>
        </div>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">

      <!-- ── Left Panel: Config ── (2/5) -->
      <div class="lg:col-span-2 space-y-5">
        <div class="card-resend space-y-7">
          <p class="text-[11px] font-semibold text-zinc-600 uppercase tracking-widest font-mono">Options</p>

          <!-- Length Slider -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-zinc-300">Length</span>
              <span class="text-sm font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-lg border border-emerald-500/20">
                {{ length }}
              </span>
            </div>
            <input
              v-model.number="length"
              type="range" min="8" max="128" step="1"
              class="range-slider w-full"
            />
            <div class="flex justify-between text-[11px] text-zinc-700 font-mono">
              <span>8</span><span>128</span>
            </div>
          </div>

          <!-- Character Types -->
          <div class="space-y-2">
            <p class="text-sm font-medium text-zinc-300 mb-3">Characters</p>
            <label
              v-for="opt in options"
              :key="opt.label"
              class="option-row"
              :class="{ 'option-row--active': opt.model.value }"
            >
              <div class="flex items-center space-x-3">
                <div
                  class="w-4 h-4 rounded flex items-center justify-center border transition-all"
                  :class="opt.model.value
                    ? 'bg-emerald-500 border-emerald-500'
                    : 'bg-transparent border-zinc-700'"
                  @click="opt.model.value = !opt.model.value"
                >
                  <svg v-if="opt.model.value" xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <span class="text-[13px] text-zinc-300 select-none" @click="opt.model.value = !opt.model.value">{{ opt.label }}</span>
              </div>
              <span class="text-[11px] font-mono text-zinc-600">{{ opt.example }}</span>
            </label>
            <p v-if="!atLeastOneSelected" class="text-xs text-red-400 pt-1">Select at least one type.</p>
          </div>

          <!-- Generate Button -->
          <button
            id="btn-generate"
            @click="generate"
            :disabled="isGenerating || !atLeastOneSelected"
            class="w-full button-primary py-3 text-[13px] font-bold flex items-center justify-center space-x-2"
          >
            <svg v-if="isGenerating" class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            <span>{{ isGenerating ? 'Generating…' : 'Generate' }}</span>
          </button>

          <p v-if="error" class="text-xs text-red-400 text-center -mt-2">{{ error }}</p>
        </div>
      </div>

      <!-- ── Right Panel: Preview ── (3/5) -->
      <div class="lg:col-span-3 space-y-5">

        <!-- Fake Login Card -->
        <div class="card-resend space-y-5">
          <!-- Fake browser chrome -->
          <div class="flex items-center space-x-1.5 mb-2">
            <div class="w-2.5 h-2.5 rounded-full bg-zinc-800"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-zinc-800"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-zinc-800"></div>
            <div class="ml-3 flex-1 bg-zinc-900 rounded px-3 py-1 flex items-center space-x-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span class="text-[10px] text-zinc-500 font-mono">vault.app · secure login</span>
            </div>
          </div>

          <p class="text-[11px] text-zinc-600 font-semibold uppercase tracking-widest font-mono">Live Preview</p>

          <!-- Fake email field -->
          <div class="space-y-1.5">
            <label class="text-[11px] font-medium text-zinc-500">Email address</label>
            <div class="input-resend flex items-center space-x-2 cursor-default opacity-60">
              <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-600 shrink-0"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              <span class="text-zinc-500 text-sm">dev@vault.com</span>
            </div>
          </div>

          <!-- Password field -->
          <div class="space-y-1.5">
            <label class="text-[11px] font-medium text-zinc-500">Password</label>
            <div
              class="input-resend flex items-center justify-between gap-3 min-h-[42px]"
              :class="{ 'border-emerald-500/30 ring-1 ring-emerald-500/10': generatedPassword }"
            >
              <span
                class="font-mono text-sm text-white truncate flex-1 transition-all duration-500 tracking-wide"
                :class="isGenerating ? 'opacity-20 blur-[3px]' : 'opacity-100'"
              >
                {{ generatedPassword ? displayedPassword : '——' }}
              </span>

              <div class="flex items-center space-x-0.5 shrink-0">
                <!-- Reveal -->
                <button
                  @click="showPassword = !showPassword"
                  class="p-1.5 rounded-lg text-zinc-600 hover:text-zinc-300 hover:bg-zinc-800 transition-colors"
                  :title="showPassword ? 'Hide' : 'Show'"
                >
                  <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                </button>

                <!-- Copy -->
                <button
                  id="btn-copy"
                  @click="copyPassword"
                  :disabled="!generatedPassword"
                  class="p-1.5 rounded-lg transition-colors"
                  :class="isCopied
                    ? 'text-emerald-400 bg-emerald-500/10'
                    : 'text-zinc-600 hover:text-zinc-300 hover:bg-zinc-800'"
                  :title="isCopied ? 'Copied!' : 'Copy'"
                >
                  <svg v-if="isCopied" xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                </button>

                <!-- Regenerate -->
                <button
                  @click="generate"
                  class="p-1.5 rounded-lg text-zinc-600 hover:text-zinc-300 hover:bg-zinc-800 transition-colors"
                  title="Regenerate"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
                </button>
              </div>
            </div>

            <!-- Copy feedback -->
            <p class="text-[11px] text-emerald-500 transition-opacity duration-200" :class="isCopied ? 'opacity-100' : 'opacity-0'">
              ✓ Copied to clipboard
            </p>
          </div>

          <!-- Strength Bar -->
          <div v-if="generatedPassword && !isGenerating" class="space-y-2 pt-1">
            <div class="flex items-center justify-between">
              <span class="text-[11px] text-zinc-600 uppercase tracking-wider font-mono">Strength</span>
              <span class="text-[11px] font-semibold font-mono" :style="{ color: strengthColor }">{{ strengthLabel }}</span>
            </div>
            <div class="h-1 bg-zinc-900 rounded-full overflow-hidden">
              <div
                class="h-full rounded-full transition-all duration-700 ease-out"
                :style="{ width: strengthPercent + '%', backgroundColor: strengthColor }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Security Metrics Card -->
        <div v-if="generatedPassword && !isGenerating" class="card-resend">
          <p class="text-[11px] font-semibold text-zinc-600 uppercase tracking-widest font-mono mb-4">Security Metrics</p>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <p class="text-[10px] text-zinc-700 uppercase tracking-wider mb-1">Entropy</p>
              <p class="text-xl font-bold font-mono text-white">
                {{ entropyScore }}<span class="text-xs font-normal text-zinc-500 ml-1">bits</span>
              </p>
            </div>
            <div>
              <p class="text-[10px] text-zinc-700 uppercase tracking-wider mb-1">Length</p>
              <p class="text-xl font-bold font-mono text-white">
                {{ generatedPassword.length }}<span class="text-xs font-normal text-zinc-500 ml-1">chars</span>
              </p>
            </div>
            <div>
              <p class="text-[10px] text-zinc-700 uppercase tracking-wider mb-1">Rating</p>
              <p class="text-sm font-bold font-mono" :style="{ color: strengthColor }">{{ strengthLabel }}</p>
            </div>
          </div>
        </div>

        <p class="text-center text-[11px] text-zinc-700">
          Passwords are generated server-side using <code class="text-zinc-500">secrets.choice</code> and never stored.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 5px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #18181b; border-radius: 10px; }

.range-slider {
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: #27272a;
  border-radius: 9999px;
  outline: none;
  cursor: pointer;
}
.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #10b981;
  border: 2px solid #000;
  box-shadow: 0 0 10px rgba(16,185,129,0.4);
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.range-slider::-webkit-slider-thumb:hover { box-shadow: 0 0 18px rgba(16,185,129,0.6); }
.range-slider::-moz-range-thumb {
  width: 18px; height: 18px; border-radius: 50%;
  background: #10b981; border: 2px solid #000; cursor: pointer;
}

.option-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 12px;
  border-radius: 10px;
  border: 1px solid #18181b;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
  user-select: none;
}
.option-row:hover { border-color: #27272a; background: #09090b; }
.option-row--active { border-color: rgba(16,185,129,0.2); background: rgba(16,185,129,0.03); }
</style>
