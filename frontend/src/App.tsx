import { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProjectsPage from './pages/ProjectsPage'
import ProjectDetailPage from './pages/ProjectDetailPage'
import KanbanBoardPage from './pages/KanbanBoardPage'
import IssueDetailPage from './pages/IssueDetailPage'
import SearchPage from './pages/SearchPage'
import NotificationsPage from './pages/NotificationsPage'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import { Toaster } from './components/ui/toaster'

function App() {
  const { isAuthenticated, fetchUser } = useAuthStore()

  useEffect(() => {
    if (isAuthenticated) {
      fetchUser()
    }
  }, [isAuthenticated, fetchUser])

  return (
    <>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/projects" replace />} />
          <Route path="projects" element={<ProjectsPage />} />
          <Route path="projects/:projectId" element={<ProjectDetailPage />} />
          <Route path="projects/:projectId/board" element={<KanbanBoardPage />} />
          <Route path="projects/:projectId/issues/:issueKey" element={<IssueDetailPage />} />
          <Route path="search" element={<SearchPage />} />
          <Route path="notifications" element={<NotificationsPage />} />
        </Route>
      </Routes>
      <Toaster />
    </>
  )
}

export default App
