import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
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
import { Plus } from 'lucide-react'
import { useToast } from '@/components/ui/use-toast'

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
                <Link key={issue.id} to={`/projects/${id}/issues/${issue.key}`}>
                  <Card className="hover:bg-muted/50 transition-colors cursor-pointer">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <span className="font-mono text-sm text-muted-foreground">
                            {issue.key}
                          </span>
                          <span className="font-medium">{issue.title}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-sm px-2 py-1 rounded bg-muted">
                            {issue.state.name}
                          </span>
                          {issue.assignee && (
                            <span className="text-sm text-muted-foreground">
                              {issue.assignee.username}
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
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Activity feed coming soon...</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings">
          <Card>
            <CardHeader>
              <CardTitle>Project Settings</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Settings coming soon...</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
