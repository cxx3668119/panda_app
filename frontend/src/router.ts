import { createRouter, createWebHistory } from 'vue-router'
import { TOKEN_STORAGE_KEY } from '@/api/client'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/daily'
    },
    {
      path: '/login',
      component: () => import('@/pages/login/index.vue'),
      meta: { public: true }
    },
    {
      path: '/profile/create',
      component: () => import('@/pages/profile/create/index.vue')
    },
    {
      path: '/profile/result',
      component: () => import('@/pages/profile/result/index.vue')
    },
    {
      path: '/daily',
      component: () => import('@/pages/daily/index/index.vue')
    },
    {
      path: '/daily/history',
      component: () => import('@/pages/daily/history/index.vue')
    },
    {
      path: '/ai/chat',
      component: () => import('@/pages/ai/chat/index.vue')
    },
    {
      path: '/growth/archive',
      component: () => import('@/pages/growth/archive/index.vue')
    },
    {
      path: '/settings/reminder',
      component: () => import('@/pages/settings/reminder/index.vue')
    }
  ]
})

router.beforeEach((to) => {
  const hasToken = !!localStorage.getItem(TOKEN_STORAGE_KEY)
  if (!to.meta.public && !hasToken) {
    return '/login'
  }
  if (to.path === '/login' && hasToken) {
    return '/daily'
  }
  return true
})

export default router
