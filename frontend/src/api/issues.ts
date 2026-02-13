import api from './client'
import type { Issue, Comment, Attachment, Event } from './types'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const issuesApi = {
  list: async (projectId: number, params?: Record<string, any>) => {
    const response = await api.get<PaginatedResponse<Issue>>(`/projects/${projectId}/issues/`, { params })
    return response.data.results
  },

  get: async (projectId: number, issueKey: string) => {
    const response = await api.get<Issue>(`/projects/${projectId}/issues/${issueKey}/`)
    return response.data
  },

  create: async (projectId: number, data: Partial<Issue>) => {
    const response = await api.post<Issue>(`/projects/${projectId}/issues/`, data)
    return response.data
  },

  update: async (projectId: number, issueKey: string, data: Partial<Issue>) => {
    const response = await api.patch<Issue>(`/projects/${projectId}/issues/${issueKey}/`, data)
    return response.data
  },

  delete: async (projectId: number, issueKey: string) => {
    await api.delete(`/projects/${projectId}/issues/${issueKey}/`)
  },

  transition: async (projectId: number, issueKey: string, toStateId: number) => {
    const response = await api.post<Issue>(
      `/projects/${projectId}/issues/${issueKey}/transitions/`,
      { to_state_id: toStateId }
    )
    return response.data
  },

  getComments: async (projectId: number, issueKey: string) => {
    const response = await api.get<PaginatedResponse<Comment>>(
      `/projects/${projectId}/issues/${issueKey}/comments/`
    )
    return response.data.results
  },

  addComment: async (projectId: number, issueKey: string, data: { content: string }) => {
    const response = await api.post<Comment>(
      `/projects/${projectId}/issues/${issueKey}/comments/`,
      data
    )
    return response.data
  },

  updateComment: async (projectId: number, issueKey: string, commentId: number, content: string) => {
    const response = await api.patch<Comment>(
      `/projects/${projectId}/issues/${issueKey}/comments/${commentId}/`,
      { content }
    )
    return response.data
  },

  deleteComment: async (projectId: number, issueKey: string, commentId: number) => {
    await api.delete(`/projects/${projectId}/issues/${issueKey}/comments/${commentId}/`)
  },

  getAttachments: async (projectId: number, issueKey: string) => {
    const response = await api.get<PaginatedResponse<Attachment>>(
      `/projects/${projectId}/issues/${issueKey}/attachments/`
    )
    return response.data.results
  },

  uploadAttachment: async (projectId: number, issueKey: string, file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post<Attachment>(
      `/projects/${projectId}/issues/${issueKey}/attachments/`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
      }
    )
    return response.data
  },

  deleteAttachment: async (projectId: number, issueKey: string, attachmentId: number) => {
    await api.delete(`/projects/${projectId}/issues/${issueKey}/attachments/${attachmentId}/`)
  },

  addWatcher: async (projectId: number, issueKey: string) => {
    await api.post(`/projects/${projectId}/issues/${issueKey}/watchers/`)
  },

  removeWatcher: async (projectId: number, issueKey: string) => {
    await api.delete(`/projects/${projectId}/issues/${issueKey}/watchers/`)
  },

  getActivity: async (projectId: number, issueKey: string) => {
    const response = await api.get<PaginatedResponse<Event>>(
      `/projects/${projectId}/issues/${issueKey}/activity/`
    )
    return response.data.results
  },

  getProjectActivity: async (projectId: number) => {
    const response = await api.get<Event[]>(`/projects/${projectId}/activity/`)
    return response.data
  },
}
