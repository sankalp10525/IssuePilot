export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  avatar?: string
  bio?: string
  created_at: string
}

export interface Project {
  id: number
  name: string
  key: string
  description: string
  icon?: string
  owner: User
  member_count: number
  created_at: string
  updated_at: string
}

export interface ProjectDetail extends Project {
  workflow: Workflow
  boards: Board[]
}

export interface ProjectMembership {
  id: number
  user: User
  role: 'owner' | 'admin' | 'member' | 'viewer'
  created_at: string
}

export interface Board {
  id: number
  name: string
  board_type: 'kanban' | 'scrum'
  created_at: string
  updated_at: string
}

export interface Sprint {
  id: number
  name: string
  goal: string
  status: 'future' | 'active' | 'closed'
  start_date?: string
  end_date?: string
  issue_count: number
  created_at: string
  updated_at: string
}

export interface Epic {
  id: number
  name: string
  description: string
  color: string
  start_date?: string
  due_date?: string
  issue_count: number
  created_at: string
  updated_at: string
}

export interface WorkflowState {
  id: number
  name: string
  category: 'todo' | 'in_progress' | 'done'
  order: number
  is_initial: boolean
  created_at: string
}

export interface WorkflowTransition {
  id: number
  from_state: WorkflowState
  to_state: WorkflowState
  name: string
  created_at: string
}

export interface Workflow {
  id: number
  name: string
  states: WorkflowState[]
  transitions: WorkflowTransition[]
  created_at: string
  updated_at: string
}

export interface Issue {
  id: number
  key: string
  sequence: number
  title: string
  description: string
  issue_type: 'task' | 'bug' | 'story' | 'epic'
  priority: 'lowest' | 'low' | 'medium' | 'high' | 'highest'
  state: WorkflowState
  reporter: User
  assignee?: User
  sprint?: number
  epic?: number
  parent?: number
  story_points?: number
  time_estimate?: number
  time_spent?: number
  due_date?: string
  resolved_at?: string
  watchers?: User[]
  is_watching?: boolean
  comment_count?: number
  attachment_count?: number
  created_at: string
  updated_at: string
}

export interface Comment {
  id: number
  content: string
  author: User
  created_at: string
  updated_at: string
}

export interface Attachment {
  id: number
  filename: string
  file_size: number
  content_type: string
  url: string
  uploaded_by: User
  created_at: string
}

export interface Notification {
  id: number
  notification_type: string
  title: string
  message: string
  project_key?: string
  issue_key?: string
  is_read: boolean
  read_at?: string
  created_at: string
}

export interface Event {
  id: number
  event_type: string
  actor: User
  issue_key?: string
  data: Record<string, any>
  created_at: string
}
