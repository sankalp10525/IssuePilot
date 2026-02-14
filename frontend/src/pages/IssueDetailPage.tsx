import { useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { issuesApi } from '@/api/issues'
import { projectsApi } from '@/api/projects'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import {
  ArrowLeft,
  Calendar,
  User,
  MessageSquare,
  Paperclip,
  Eye,
  Trash2,
  Send,
} from 'lucide-react'
import { formatDate, formatDateTime } from '@/lib/utils'
import { useToast } from '@/components/ui/use-toast'
import type { Issue } from '@/api/types'

export default function IssueDetailPage() {
  const { projectId, issueKey } = useParams<{ projectId: string; issueKey: string }>()
  const navigate = useNavigate()
  const { toast } = useToast()
  const queryClient = useQueryClient()
  const id = parseInt(projectId!)

  const [commentContent, setCommentContent] = useState('')
  const [editingDescription, setEditingDescription] = useState(false)
  const [description, setDescription] = useState('')

  const { data: project } = useQuery({
    queryKey: ['project', id],
    queryFn: () => projectsApi.get(id),
  })

  const { data: issue, isLoading } = useQuery({
    queryKey: ['issue', id, issueKey],
    queryFn: () => issuesApi.get(id, issueKey!),
    enabled: !!issueKey,
  })

  const { data: comments } = useQuery({
    queryKey: ['issue-comments', id, issueKey],
    queryFn: () => issuesApi.getComments(id, issueKey!),
    enabled: !!issueKey,
  })

  const { data: attachments } = useQuery({
    queryKey: ['issue-attachments', id, issueKey],
    queryFn: () => issuesApi.getAttachments(id, issueKey!),
    enabled: !!issueKey,
  })

  const { data: members } = useQuery({
    queryKey: ['project-members', id],
    queryFn: () => projectsApi.getMembers(id),
  })

  const updateIssueMutation = useMutation({
    mutationFn: (data: Partial<Issue>) => issuesApi.update(id, issueKey!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['issue', id, issueKey] })
      queryClient.invalidateQueries({ queryKey: ['issues', id] })
      toast({ title: 'Success', description: 'Issue updated successfully' })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to update issue',
        variant: 'destructive',
      })
    },
  })

  const addCommentMutation = useMutation({
    mutationFn: (content: string) => issuesApi.addComment(id, issueKey!, { content }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['issue-comments', id, issueKey] })
      queryClient.invalidateQueries({ queryKey: ['issue', id, issueKey] })
      setCommentContent('')
      toast({ title: 'Success', description: 'Comment added successfully' })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to add comment',
        variant: 'destructive',
      })
    },
  })

  const toggleWatchMutation = useMutation({
    mutationFn: () => {
      return issue?.is_watching
        ? issuesApi.removeWatcher(id, issueKey!)
        : issuesApi.addWatcher(id, issueKey!)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['issue', id, issueKey] })
      toast({
        title: 'Success',
        description: issue?.is_watching ? 'Stopped watching issue' : 'Now watching issue',
      })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to update watch status',
        variant: 'destructive',
      })
    },
  })

  const deleteIssueMutation = useMutation({
    mutationFn: () => issuesApi.delete(id, issueKey!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['issues', id] })
      toast({ title: 'Success', description: 'Issue deleted successfully' })
      navigate(`/projects/${id}`)
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to delete issue',
        variant: 'destructive',
      })
    },
  })

  const transitionMutation = useMutation({
    mutationFn: ({ toStateId }: { toStateId: number }) =>
      issuesApi.transition(id, issueKey!, toStateId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['issue', id, issueKey] })
      queryClient.invalidateQueries({ queryKey: ['issues', id] })
      toast({ title: 'Success', description: 'Issue status updated successfully' })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to update status',
        variant: 'destructive',
      })
    },
  })

  const handleUpdateField = (field: keyof Issue, value: any) => {
    updateIssueMutation.mutate({ [field]: value })
  }

  const handleAddComment = (e: React.FormEvent) => {
    e.preventDefault()
    if (commentContent.trim()) {
      addCommentMutation.mutate(commentContent)
    }
  }

  const handleUpdateDescription = () => {
    updateIssueMutation.mutate({ description })
    setEditingDescription(false)
  }

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      highest: 'bg-red-500',
      high: 'bg-orange-500',
      medium: 'bg-yellow-500',
      low: 'bg-blue-500',
      lowest: 'bg-gray-500',
    }
    return colors[priority] || 'bg-gray-500'
  }

  const getTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      bug: '🐛',
      task: '✓',
      story: '📖',
      epic: '⚡',
    }
    return icons[type] || '📋'
  }

  if (isLoading) {
    return <div className="text-center py-12">Loading issue...</div>
  }

  if (!issue) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground mb-4">Issue not found</p>
        <Button onClick={() => navigate(`/projects/${id}`)}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Project
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-gradient-to-r from-muted/50 to-transparent p-6 rounded-lg -mx-6 mb-2">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate(`/projects/${id}`)} className="hover:bg-background/80">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
          <div>
            <div className="flex items-center gap-3">
              <span className="text-3xl">{getTypeIcon(issue.issue_type)}</span>
              <h1 className="text-3xl font-bold">{issue.title}</h1>
            </div>
            <p className="text-sm text-muted-foreground mt-2 flex items-center gap-2">
              <span className="font-mono bg-muted px-2 py-0.5 rounded">{issue.key}</span>
              <span>•</span>
              <span>Created {formatDate(issue.created_at)}</span>
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant={issue.is_watching ? 'default' : 'outline'}
            size="sm"
            onClick={() => toggleWatchMutation.mutate()}
            disabled={toggleWatchMutation.isPending}
          >
            <Eye className="mr-2 h-4 w-4" />
            {issue.is_watching ? 'Watching' : 'Watch'}
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={() => {
              if (confirm('Are you sure you want to delete this issue?')) {
                deleteIssueMutation.mutate()
              }
            }}
            disabled={deleteIssueMutation.isPending}
          >
            <Trash2 className="mr-2 h-4 w-4" />
            Delete
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Description */}
          <Card className="border-l-4 border-l-primary/20 hover:border-l-primary/40 transition-colors">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg">Description</CardTitle>
            </CardHeader>
            <CardContent>
              {editingDescription ? (
                <div className="space-y-2">
                  <Textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={6}
                    placeholder="Add a description..."
                  />
                  <div className="flex gap-2">
                    <Button size="sm" onClick={handleUpdateDescription}>
                      Save
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setEditingDescription(false)}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <div
                  className="prose prose-sm max-w-none cursor-pointer hover:bg-muted/50 p-2 rounded"
                  onClick={() => {
                    setDescription(issue.description || '')
                    setEditingDescription(true)
                  }}
                >
                  {issue.description ? (
                    <p className="whitespace-pre-wrap">{issue.description}</p>
                  ) : (
                    <p className="text-muted-foreground italic">Click to add a description...</p>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Comments */}
          <Card className="border-l-4 border-l-blue-500/20 hover:border-l-blue-500/40 transition-colors">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center gap-2">
                <MessageSquare className="h-5 w-5 text-blue-500" />
                Comments
                <span className="text-sm font-normal text-muted-foreground">({comments?.length || 0})</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Add Comment Form */}
              <form onSubmit={handleAddComment} className="space-y-2">
                <Textarea
                  placeholder="Add a comment..."
                  value={commentContent}
                  onChange={(e) => setCommentContent(e.target.value)}
                  rows={3}
                />
                <Button
                  type="submit"
                  size="sm"
                  disabled={!commentContent.trim() || addCommentMutation.isPending}
                >
                  <Send className="mr-2 h-4 w-4" />
                  {addCommentMutation.isPending ? 'Adding...' : 'Add Comment'}
                </Button>
              </form>

              <Separator />

              {/* Comments List */}
              <div className="space-y-4">
                {comments?.map((comment) => (
                  <div key={comment.id} className="flex gap-3 p-3 rounded-lg hover:bg-muted/30 transition-colors group">
                    <Avatar className="ring-2 ring-muted group-hover:ring-primary/20 transition-all">
                      <AvatarFallback className="bg-gradient-to-br from-primary/20 to-primary/10 font-semibold">
                        {comment.author.username.substring(0, 2).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-sm group-hover:text-primary transition-colors">
                          {comment.author.full_name || comment.author.username}
                        </span>
                        <span className="text-xs text-muted-foreground bg-muted px-2 py-0.5 rounded">
                          {formatDateTime(comment.created_at)}
                        </span>
                      </div>
                      <p className="text-sm whitespace-pre-wrap leading-relaxed">{comment.content}</p>
                    </div>
                  </div>
                ))}
                {comments?.length === 0 && (
                  <p className="text-sm text-muted-foreground text-center py-4">
                    No comments yet. Be the first to comment!
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Attachments */}
          {attachments && attachments.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Paperclip className="h-5 w-5" />
                  Attachments ({attachments.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {attachments.map((attachment) => (
                    <a
                      key={attachment.id}
                      href={attachment.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 p-2 hover:bg-muted rounded text-sm"
                    >
                      <Paperclip className="h-4 w-4" />
                      <span>{attachment.filename}</span>
                      <span className="text-xs text-muted-foreground ml-auto">
                        {(attachment.file_size / 1024).toFixed(1)} KB
                      </span>
                    </a>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Status */}
          <Card className="border-2 hover:shadow-md transition-all">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">Status</CardTitle>
            </CardHeader>
            <CardContent>
              <Select
                value={issue.state.id.toString()}
                onValueChange={(value) => {
                  const toStateId = parseInt(value)
                  transitionMutation.mutate({ toStateId })
                }}
              >
                <SelectTrigger>
                  <SelectValue>
                    <Badge variant="outline" className="w-full justify-center py-1 text-sm font-semibold">
                      {issue.state.name}
                    </Badge>
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  {project?.workflow.states.map((state) => (
                    <SelectItem key={state.id} value={state.id.toString()}>
                      {state.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          {/* Details */}
          <Card className="border-2 hover:shadow-md transition-all">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Priority */}
              <div className="space-y-2">
                <Label className="text-xs text-muted-foreground">Priority</Label>
                <Select
                  value={issue.priority}
                  onValueChange={(value) => handleUpdateField('priority', value)}
                >
                  <SelectTrigger>
                    <SelectValue>
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${getPriorityColor(issue.priority)}`} />
                        <span className="capitalize">{issue.priority}</span>
                      </div>
                    </SelectValue>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="highest">Highest</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="low">Low</SelectItem>
                    <SelectItem value="lowest">Lowest</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Assignee */}
              <div className="space-y-2">
                <Label className="text-xs text-muted-foreground">Assignee</Label>
                <Select
                  value={issue.assignee?.id.toString() || 'unassigned'}
                  onValueChange={(value) =>
                    handleUpdateField('assignee_id', value === 'unassigned' ? null : parseInt(value))
                  }
                >
                  <SelectTrigger>
                    <SelectValue>
                      {issue.assignee ? (
                        <div className="flex items-center gap-2">
                          <User className="h-4 w-4" />
                          <span>{issue.assignee.full_name || issue.assignee.username}</span>
                        </div>
                      ) : (
                        <span className="text-muted-foreground">Unassigned</span>
                      )}
                    </SelectValue>
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

              {/* Reporter */}
              <div className="space-y-2">
                <Label className="text-xs text-muted-foreground">Reporter</Label>
                <div className="flex items-center gap-2 text-sm">
                  <User className="h-4 w-4" />
                  <span>{issue.reporter.full_name || issue.reporter.username}</span>
                </div>
              </div>

              {/* Type */}
              <div className="space-y-2">
                <Label className="text-xs text-muted-foreground">Type</Label>
                <div className="flex items-center gap-2 text-sm">
                  <span>{getTypeIcon(issue.issue_type)}</span>
                  <span className="capitalize">{issue.issue_type}</span>
                </div>
              </div>

              {/* Story Points */}
              {issue.story_points && (
                <div className="space-y-2">
                  <Label className="text-xs text-muted-foreground">Story Points</Label>
                  <div className="text-sm font-medium">{issue.story_points}</div>
                </div>
              )}

              {/* Due Date */}
              {issue.due_date && (
                <div className="space-y-2">
                  <Label className="text-xs text-muted-foreground">Due Date</Label>
                  <div className="flex items-center gap-2 text-sm">
                    <Calendar className="h-4 w-4" />
                    <span>{formatDate(issue.due_date)}</span>
                  </div>
                </div>
              )}

              {/* Watchers */}
              {issue.watchers && issue.watchers.length > 0 && (
                <div className="space-y-2">
                  <Label className="text-xs text-muted-foreground">
                    Watchers ({issue.watchers.length})
                  </Label>
                  <div className="flex flex-wrap gap-1">
                    {issue.watchers.map((watcher) => (
                      <Badge key={watcher.id} variant="secondary" className="text-xs">
                        {watcher.username}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Links */}
          {project && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Links</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Link
                  to={`/projects/${id}`}
                  className="text-sm text-blue-600 hover:underline block"
                >
                  View Project: {project.name}
                </Link>
                <Link
                  to={`/projects/${id}/board`}
                  className="text-sm text-blue-600 hover:underline block"
                >
                  View on Board
                </Link>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
