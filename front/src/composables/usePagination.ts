import { ref, computed } from 'vue'

export function usePagination(initialLimit = 20) {
    const page = ref(1)
    const limit = ref(initialLimit)
    const total = ref(0)
    const pages = ref(0)

    const offset = computed(() => (page.value - 1) * limit.value)
    const hasNext = computed(() => page.value < pages.value)
    const hasPrev = computed(() => page.value > 1)

    const startItem = computed(() => (page.value - 1) * limit.value + 1)
    const endItem = computed(() => Math.min(page.value * limit.value, total.value))

    const setPagination = (data: { total: number, page: number, limit: number, pages: number }) => {
        total.value = data.total
        page.value = data.page
        limit.value = data.limit
        pages.value = data.pages
    }

    return {
        page,
        limit,
        total,
        pages,
        offset,
        hasNext,
        hasPrev,
        startItem,
        endItem,
        setPagination
    }
}
