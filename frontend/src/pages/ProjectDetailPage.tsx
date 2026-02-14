import { useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { projectsApi } from '@/api/projects'
import { issuesApi } from '@/api/issues'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Plus, Clock, User, GitBranch, MessageSquare, Paperclip, UserPlus, Calendar, Trash2, Settings } from 'lucide-react'
import { useToast } from '@/components/ui/use-toast'
import type { Event, ProjectDetail } from '@/api/types'

function ActivityFeed({ projectId }: { projectId: number }) {
  const { data: events, isLoading } = useQuery({
    queryKey: ['project-activity', projectId],
    queryFn: () => projectsApi.getActivity(projectId),
  })

  const getEventIcon = (eventType: string) => {
    const icons: Record<string, JSX.Element> = {
      issue_created: <Plus className="h-4 w-4 text-green-500" />,
      issue_updated: <GitBranch className="h-4 w-4 text-blue-500" />,
      issue_deleted: <Plus className="h-4 w-4 text-red-500" />,
      state_changed: <GitBranch className="h-4 w-4 text-purple-500" />,
      comment_added: <MessageSquare className="h-4 w-4 text-blue-500" />,
      attachment_added: <Paperclip className="h-4 w-4 text-gray-500" />,
      assignee_changed: <UserPlus className="h-4 w-4 text-orange-500" />,
      sprint_changed: <Calendar className="h-4 w-4 text-indigo-500" />,
    }
    return icons[eventType] || <Clock className="h-4 w-4" />
  }

  const getEventMessage = (event: Event) => {
    const actorName = event.actor?.full_name || event.actor?.username || 'Someone'
    
    switch (event.event_type) {
      case 'issue_created':
        return `${actorName} created issue`
      case 'issue_updated':
        return `${actorName} updated issue`
      case 'issue_deleted':
        return `${actorName} deleted issue`
      case 'state_changed':
        return `${actorName} changed state to ${event.data.to_state || 'a new state'}`
      case 'comment_added':
        return `${actorName} added a comment`
      case 'attachment_added':
        return `${actorName} added an attachment`
      case 'assignee_changed':
        return `${actorName} changed the assignee`
      case 'sprint_changed':
        return `${actorName} moved to ${event.data.sprint_name || 'a sprint'}`
      default:
        return `${actorName} performed an action`
    }
  }

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = Math.floor((now.getTime() - date.getTime()) / 1000)

    if (diff < 60) return 'just now'
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
    if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
    return date.toLocaleDateString()
  }

  if (isLoading) {
    return (
      <Card>
        <CardContent className="py-12 text-center text-muted-foreground">
          Loading activity...
        </CardContent>
      </Card>
    )
  }

  if (!events || events.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-8">No activity yet</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
        <CardDescription>Latest events in this project</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {events.map((event) => (
            <div
              key={event.id}
              className="flex gap-3 p-3 rounded-lg border border-border/50 hover:bg-muted/30 transition-colors"
            >
              <div className="flex-shrink-0 mt-1">{getEventIcon(event.event_type)}</div>
              <div className="flex-1 min-w-0 space-y-1">
                <div className="flex items-start justify-between gap-2">
                  <p className="text-sm">
                    {getEventMessage(event)}
                    {event.issue_key && (
                      <Link
                        to={`/projects/${projectId}/issues/${event.issue_key}`}
                        className="ml-1 font-mono text-primary hover:underline"
                      >
                        {event.issue_key}
                      </Link>
                    )}
                  </p>
                  <span className="text-xs text-muted-foreground whitespace-nowrap">
                    {formatTime(event.created_at)}
                  </span>
                </div>
                {event.actor && (
                  <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                    <User className="h-3 w-3" />
                    <span>{event.actor.full_name || event.actor.username}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

function ProjectSettings({ projectId, project }: { projectId: number; project: ProjectDetail }) {
  const navigate = useNavigate()
  const { toast } = useToast()
  const queryClient = useQueryClient()
  
  const [editFormData, setEditFormData] = useState({
    name: project.name,
    description: project.description,
    icon: project.icon || '',
  })
  
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false)

  const updateMutation = useMutation({
    mutationFn: (data: typeof editFormData) => projectsApi.update(projectId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['project', projectId] })
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      toast({
        title: 'Success',
        description: 'Project updated successfully',
      })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to update project',
        variant: 'destructive',
      })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: () => projectsApi.delete(projectId),
    onSuccess: () => {
      toast({
        title: 'Success',
        description: 'Project deleted successfully',
      })
      navigate('/projects')
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to delete project',
        variant: 'destructive',
      })
    },
  })

  const handleUpdate = (e: React.FormEvent) => {
    e.preventDefault()
    updateMutation.mutate(editFormData)
  }

  const handleDelete = () => {
    deleteMutation.mutate()
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>General Settings</CardTitle>
          <CardDescription>Update your project information</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleUpdate} className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="name">Project Name</Label>
              <Input
                id="name"
                value={editFormData.name}
                onChange={(e) => setEditFormData({ ...editFormData, name: e.target.value })}
                placeholder="Enter project name"
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="icon">Icon Emoji</Label>
              <Input
                id="icon"
                value={editFormData.icon}
                onChange={(e) => setEditFormData({ ...editFormData, icon: e.target.value })}
                placeholder="e.g., 🚀"
                maxLength={2}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={editFormData.description}
                onChange={(e) => setEditFormData({ ...editFormData, description: e.target.value })}
                placeholder="Describe your project"
                rows={4}
              />
            </div>
            <Button type="submit" disabled={updateMutation.isPending}>
              {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card className="border-red-200 dark:border-red-900">
        <CardHeader>
          <CardTitle className="text-red-600 dark:text-red-400">Danger Zone</CardTitle>
          <CardDescription>Irreversible actions</CardDescription>
        </CardHeader>
        <CardContent>
          <Dialog open={deleteConfirmOpen} onOpenChange={setDeleteConfirmOpen}>
            <DialogTrigger asChild>
              <Button variant="destructive" className="gap-2">
                <Trash2 className="h-4 w-4" />
                Delete Project
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Are you absolutely sure?</DialogTitle>
                <DialogDescription className="space-y-2">
                  <p>This action cannot be undone. This will permanently delete the project:</p>
                  <p className="font-semibold text-foreground">
                    {project.icon} {project.name} ({project.key})
                  </p>
                  <p>All issues, comments, and related data will be lost.</p>
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button variant="outline" onClick={() => setDeleteConfirmOpen(false)}>
                  Cancel
                </Button>
                <Button
                  variant="destructive"
                  onClick={handleDelete}
                  disabled={deleteMutation.isPending}
                >
                  {deleteMutation.isPending ? 'Deleting...' : 'Delete Project'}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </CardContent>
      </Card>
    </div>
  )
}

export default function ProjectDetailPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const id = parseInt(projectId!)
  
  const [issueDialogOpen, setIssueDialogOpen] = useState(false)
  const [issueFormData, setIssueFormData] = useState({
    title: '',
    description: '',
    issue_type: 'task' as 'task' | 'bug' | 'story' | 'epic',
    priority: 'medium' as 'lowest' | 'low' | 'medium' | 'high' | 'highest',
    assignee_id: undefined as number | undefined,
  })

  const { toast } = useToast()
  const queryClient = useQueryClient()

  const { data: project, isLoading: projectLoading } = useQuery({
    queryKey: ['project', id],
    queryFn: () => projectsApi.get(id),
  })

  const { data: issues, isLoading: issuesLoading } = useQuery({
    queryKey: ['issues', id],
    queryFn: () => issuesApi.list(id),
  })
  
  const { data: members } = useQuery({
    queryKey: ['project-members', id],
    queryFn: () => projectsApi.getMembers(id),
  })

  const createIssueMutation = useMutation({
    mutationFn: (data: typeof issueFormData) => issuesApi.create(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['issues', id] })
      toast({
        title: 'Success',
        description: 'Issue created successfully',
      })
      setIssueDialogOpen(false)
      setIssueFormData({
        title: '',
        description: '',
        issue_type: 'task',
        priority: 'medium',
        assignee_id: undefined,
      })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to create issue',
        variant: 'destructive',
      })
    },
  })

  const handleIssueSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createIssueMutation.mutate(issueFormData)
  }

  const handleIssueChange = (field: string, value: any) => {
    setIssueFormData({ ...issueFormData, [field]: value })
  }

  if (projectLoading) {
    return <div className="text-center py-12">Loading project...</div>
  }

  if (!project) {
    return <div className="text-center py-12">Project not found</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            {project.icon && <span className="text-3xl">{project.icon}</span>}
            <div>
              <h1 className="text-3xl font-bold">{project.name}</h1>
              <p className="text-muted-foreground">{project.key}</p>
            </div>
          </div>
          <p className="mt-2 text-muted-foreground">{project.description}</p>
        </div>
        <Link to={`/projects/${id}/board`}>
          <Button>View Board</Button>
        </Link>
      </div>

      <Tabs defaultValue="issues" className="w-full">
        <TabsList>
          <TabsTrigger value="issues">Issues</TabsTrigger>
          <TabsTrigger value="board">Board</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="issues" className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Issues</h2>
            <Dialog open={issueDialogOpen} onOpenChange={setIssueDialogOpen}>
              <DialogTrigger asChild>
                <Button size="sm">
                  <Plus className="mr-2 h-4 w-4" />
                  Create Issue
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[525px]">
                <form onSubmit={handleIssueSubmit}>
                  <DialogHeader>
                    <DialogTitle>Create New Issue</DialogTitle>
                    <DialogDescription>
                      Add a new issue to track work in your project.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid gap-2">
                      <Label htmlFor="title">Title</Label>
                      <Input
                        id="title"
                        placeholder="Issue title"
                        value={issueFormData.title}
                        onChange={(e) => handleIssueChange('title', e.target.value)}
                        required
                      />
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="description">Description</Label>
                      <Textarea
                        id="description"
                        placeholder="Describe the issue..."
                        value={issueFormData.description}
                        onChange={(e) => handleIssueChange('description', e.target.value)}
                        rows={4}
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="grid gap-2">
                        <Label htmlFor="issue_type">Type</Label>
                        <Select
                          value={issueFormData.issue_type}
                          onValueChange={(value) => handleIssueChange('issue_type', value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="task">Task</SelectItem>
                            <SelectItem value="bug">Bug</SelectItem>
                            <SelectItem value="story">Story</SelectItem>
                            <SelectItem value="epic">Epic</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="priority">Priority</Label>
                        <Select
                          value={issueFormData.priority}
                          onValueChange={(value) => handleIssueChange('priority', value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select priority" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="lowest">Lowest</SelectItem>
                            <SelectItem value="low">Low</SelectItem>
                            <SelectItem value="medium">Medium</SelectItem>
                            <SelectItem value="high">High</SelectItem>
                            <SelectItem value="highest">Highest</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="assignee">Assignee (Optional)</Label>
                      <Select
                        value={issueFormData.assignee_id?.toString() || 'unassigned'}
                        onValueChange={(value) => handleIssueChange('assignee_id', value === 'unassigned' ? undefined : parseInt(value))}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Unassigned" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="unassigned">Unassigned</SelectItem>
                          {members?.map((member) => (
                            <SelectItem key={member.user.id} value={member.user.id.toString()}>
                              {member.user.full_name || member.user.username}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  <DialogFooter>
                    <Button type="button" variant="outline" onClick={() => setIssueDialogOpen(false)}>
                      Cancel
                    </Button>
                    <Button type="submit" disabled={createIssueMutation.isPending}>
                      {createIssueMutation.isPending ? 'Creating...' : 'Create Issue'}
                    </Button>
                  </DialogFooter>
                </form>
              </DialogContent>
            </Dialog>
          </div>

          {issuesLoading ? (
            <div>Loading issues...</div>
          ) : (
            <div className="space-y-2">
              {issues?.map((issue) => (
                <Link key={issue.id} to={`/projects/${id}/issues/${issue.key}`} className="group">
                  <Card className="hover:bg-muted/30 hover:shadow-md transition-all duration-200 cursor-pointer border-l-4 border-l-transparent hover:border-l-primary">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3 flex-1 min-w-0">
                          <span className="font-mono text-xs text-muted-foreground bg-muted px-2 py-1 rounded group-hover:bg-primary/10 transition-colors">
                            {issue.key}
                          </span>
                          <span className="font-medium group-hover:text-primary transition-colors truncate">{issue.title}</span>
                        </div>
                        <div className="flex items-center gap-2 flex-shrink-0">
                          <span className="text-xs px-2.5 py-1 rounded-full bg-muted font-medium group-hover:bg-primary/10 transition-colors">
                            {issue.state.name}
                          </span>
                          {issue.assignee && (
                            <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded-full group-hover:bg-muted/70 transition-colors">
                              @{issue.assignee.username}
                            </span>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          )}

          {issues?.length === 0 && (
            <div className="text-center py-12 text-muted-foreground">
              No issues yet. Create your first issue to get started.
            </div>
          )}
        </TabsContent>

        <TabsContent value="board">
          <Card>
            <CardHeader>
              <CardTitle>Kanban Board</CardTitle>
              <CardDescription>Drag and drop issues to update their status</CardDescription>
            </CardHeader>
            <CardContent>
              <Link to={`/projects/${id}/board`}>
                <Button>Go to Board View</Button>
              </Link>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="activity">
          <ActivityFeed projectId={id} />
        </TabsContent>

        <TabsContent value="settings">
          <ProjectSettings projectId={id} project={project!} />
        </TabsContent>
      </Tabs>
    </div>
  )
}
