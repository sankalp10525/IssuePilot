import api from './client'
import type { Notification } from './types'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const notificationsApi = {
  list: async (isRead?: boolean) => {
    const params = isRead !== undefined ? { is_read: isRead } : {}
    const response = await api.get<PaginatedResponse<Notification>>('/notifications/', { params })
    return response.data.results
  },

  markAsRead: async (id: number) => {
    const response = await api.patch<Notification>(`/notifications/${id}/`, { is_read: true })
    return response.data
  },

  markAllAsRead: async () => {
    const response = await api.post('/notifications/mark-all-read/')
    return response.data
  },

  getUnreadCount: async () => {
    const response = await api.get<{ count: number }>('/notifications/unread-count/')
    return response.data
  },
}
