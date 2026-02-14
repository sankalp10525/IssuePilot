import api from './client'
import type { User } from './types'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access: string
  refresh: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name?: string
  last_name?: string
}

export interface RegisterResponse {
  user: User
  tokens: {
    access: string
    refresh: string
  }
}

export const authApi = {
  login: async (data: LoginRequest) => {
    const response = await api.post<LoginResponse>('/auth/login/', data)
    return response.data
  },

  register: async (data: RegisterRequest) => {
    const response = await api.post<RegisterResponse>('/auth/register/', data)
    return response.data
  },

  getMe: async () => {
    const response = await api.get<User>('/auth/me/')
    return response.data
  },

  updateMe: async (data: Partial<User>) => {
    const response = await api.patch<User>('/auth/me/', data)
    return response.data
  },
}
