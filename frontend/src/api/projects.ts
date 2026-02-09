import api from './client'
import type { Project, ProjectDetail, ProjectMembership, Board, Epic, Sprint, Workflow } from './types'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const projectsApi = {
  list: async () => {
    const response = await api.get<PaginatedResponse<Project>>('/projects/')
    return response.data.results
  },

  get: async (id: number) => {
    const response = await api.get<ProjectDetail>(`/projects/${id}/`)
    return response.data
  },

  create: async (data: { name: string; key: string; description?: string; icon?: string }) => {
    const response = await api.post<Project>('/projects/', data)
    return response.data
  },

  update: async (id: number, data: Partial<Project>) => {
    const response = await api.patch<Project>(`/projects/${id}/`, data)
    return response.data
  },

  delete: async (id: number) => {
    await api.delete(`/projects/${id}/`)
  },

  getMembers: async (projectId: number) => {
    const response = await api.get<PaginatedResponse<ProjectMembership>>(`/projects/${projectId}/members/`)
    return response.data.results
  },

  addMember: async (projectId: number, userId: number, role: string) => {
    const response = await api.post<ProjectMembership>(`/projects/${projectId}/members/`, {
      user_id: userId,
      role,
    })
    return response.data
  },

  removeMember: async (projectId: number, membershipId: number) => {
    await api.delete(`/projects/${projectId}/members/${membershipId}/`)
  },

  getBoards: async (projectId: number) => {
    const response = await api.get<PaginatedResponse<Board>>(`/projects/${projectId}/boards/`)
    return response.data.results
  },

  createBoard: async (projectId: number, data: { name: string; board_type: string }) => {
    const response = await api.post<Board>(`/projects/${projectId}/boards/`, data)
    return response.data
  },

  getEpics: async (projectId: number) => {
    const response = await api.get<PaginatedResponse<Epic>>(`/projects/${projectId}/epics/`)
    return response.data.results
  },

  createEpic: async (projectId: number, data: Partial<Epic>) => {
    const response = await api.post<Epic>(`/projects/${projectId}/epics/`, data)
    return response.data
  },

  getWorkflow: async (projectId: number) => {
    const response = await api.get<Workflow>(`/projects/${projectId}/workflow/`)
    return response.data
  },

  getSprints: async (boardId: number, status?: string) => {
    const params = status ? { status } : {}
    const response = await api.get<PaginatedResponse<Sprint>>(`/boards/${boardId}/sprints/`, { params })
    return response.data.results
  },

  createSprint: async (boardId: number, data: Partial<Sprint>) => {
    const response = await api.post<Sprint>(`/boards/${boardId}/sprints/`, data)
    return response.data
  },

  startSprint: async (boardId: number, sprintId: number) => {
    const response = await api.post<Sprint>(`/boards/${boardId}/sprints/${sprintId}/start/`)
    return response.data
  },

  closeSprint: async (boardId: number, sprintId: number) => {
    const response = await api.post<Sprint>(`/boards/${boardId}/sprints/${sprintId}/close/`)
    return response.data
  },
}
