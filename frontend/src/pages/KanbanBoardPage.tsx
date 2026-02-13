import { useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  DndContext,
  DragOverlay,
  closestCorners,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragStartEvent,
  DragEndEvent,
} from '@dnd-kit/core'
import { arrayMove, SortableContext, sortableKeyboardCoordinates } from '@dnd-kit/sortable'
import { issuesApi } from '@/api/issues'
import { projectsApi } from '@/api/projects'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, Plus } from 'lucide-react'
import { useToast } from '@/components/ui/use-toast'
import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import type { Issue, WorkflowState } from '@/api/types'

interface IssueCardProps {
  issue: Issue
}

function IssueCard({ issue }: IssueCardProps) {
  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      highest: 'border-l-red-500',
      high: 'border-l-orange-500',
      medium: 'border-l-yellow-500',
      low: 'border-l-blue-500',
      lowest: 'border-l-gray-500',
    }
    return colors[priority] || 'border-l-gray-500'
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

  return (
    <div className={`border-l-4 ${getPriorityColor(issue.priority)}`}>
      <Card className="cursor-move hover:shadow-md transition-shadow">
        <CardContent className="p-3 space-y-2">
          <div className="flex items-start justify-between gap-2">
            <span className="text-xs font-mono text-muted-foreground">{issue.key}</span>
            <span className="text-lg">{getTypeIcon(issue.issue_type)}</span>
          </div>
          <h4 className="text-sm font-medium line-clamp-2">{issue.title}</h4>
          <div className="flex items-center justify-between">
            <Badge variant="outline" className="text-xs capitalize">
              {issue.priority}
            </Badge>
            {issue.assignee && (
              <div className="text-xs text-muted-foreground">
                @{issue.assignee.username}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function SortableIssueCard({ issue }: IssueCardProps) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: issue.id,
    data: {
      type: 'issue',
      issue,
    },
  })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  }

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <Link to={`/projects/${issue.project_id}/issues/${issue.key}`}>
        <IssueCard issue={issue} />
      </Link>
    </div>
  )
}

interface ColumnProps {
  state: WorkflowState
  issues: Issue[]
}

function Column({ state, issues }: ColumnProps) {
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      todo: 'bg-gray-100 dark:bg-gray-800',
      in_progress: 'bg-blue-50 dark:bg-blue-950',
      done: 'bg-green-50 dark:bg-green-950',
    }
    return colors[category] || 'bg-gray-100'
  }

  return (
    <div className={`flex flex-col rounded-lg ${getCategoryColor(state.category)} p-4 min-w-[300px]`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h3 className="font-semibold">{state.name}</h3>
          <Badge variant="secondary">{issues.length}</Badge>
        </div>
      </div>
      
      <SortableContext items={issues.map((i) => i.id)}>
        <div className="space-y-2 flex-1">
          {issues.map((issue) => (
            <SortableIssueCard key={issue.id} issue={issue} />
          ))}
          {issues.length === 0 && (
            <div className="text-sm text-muted-foreground text-center py-8">
              No issues
            </div>
          )}
        </div>
      </SortableContext>
    </div>
  )
}

export default function KanbanBoardPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const { toast } = useToast()
  const queryClient = useQueryClient()
  const id = parseInt(projectId!)

  const [activeIssue, setActiveIssue] = useState<Issue | null>(null)

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  )

  const { data: project } = useQuery({
    queryKey: ['project', id],
    queryFn: () => projectsApi.get(id),
  })

  const { data: issues, isLoading } = useQuery({
    queryKey: ['issues', id],
    queryFn: () => issuesApi.list(id),
  })

  const transitionMutation = useMutation({
    mutationFn: ({ issueKey, toStateId }: { issueKey: string; toStateId: number }) =>
      issuesApi.transition(id, issueKey, toStateId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['issues', id] })
      toast({
        title: 'Success',
        description: 'Issue moved successfully',
      })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to move issue',
        variant: 'destructive',
      })
      // Revert the optimistic update
      queryClient.invalidateQueries({ queryKey: ['issues', id] })
    },
  })

  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event
    const issue = active.data.current?.issue as Issue
    setActiveIssue(issue)
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    setActiveIssue(null)

    if (!over) return

    const activeIssue = active.data.current?.issue as Issue
    const overStateId = over.data.current?.stateId as number

    if (activeIssue && overStateId && activeIssue.state.id !== overStateId) {
      // Optimistically update the UI
      queryClient.setQueryData(['issues', id], (oldIssues: Issue[] | undefined) => {
        if (!oldIssues) return oldIssues
        return oldIssues.map((issue) =>
          issue.id === activeIssue.id
            ? {
                ...issue,
                state: project?.workflow.states.find((s) => s.id === overStateId) || issue.state,
              }
            : issue
        )
      })

      // Make the API call
      transitionMutation.mutate({
        issueKey: activeIssue.key,
        toStateId: overStateId,
      })
    }
  }

  if (isLoading) {
    return <div className="text-center py-12">Loading board...</div>
  }

  if (!project || !issues) {
    return <div className="text-center py-12">Failed to load board</div>
  }

  // Group issues by state
  const issuesByState: Record<number, Issue[]> = {}
  project.workflow.states.forEach((state) => {
    issuesByState[state.id] = issues.filter((issue) => issue.state.id === state.id)
  })

  // Sort states by order
  const sortedStates = [...project.workflow.states].sort((a, b) => a.order - b.order)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate(`/projects/${id}`)}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Project
          </Button>
          <div>
            <h1 className="text-3xl font-bold">{project.name} Board</h1>
            <p className="text-sm text-muted-foreground mt-1">
              Drag and drop issues to change their status
            </p>
          </div>
        </div>
        <Button onClick={() => navigate(`/projects/${id}`)}>
          <Plus className="mr-2 h-4 w-4" />
          Create Issue
        </Button>
      </div>

      {/* Kanban Board */}
      <DndContext
        sensors={sensors}
        collisionDetection={closestCorners}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
      >
        <div className="flex gap-4 overflow-x-auto pb-4">
          {sortedStates.map((state) => (
            <div
              key={state.id}
              data-state-id={state.id}
              className="flex-shrink-0"
            >
              <SortableContext items={issuesByState[state.id]?.map((i) => i.id) || []}>
                <div
                  data-state-id={state.id}
                  className="droppable"
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault()
                    const targetElement = e.currentTarget as HTMLElement
                    const stateId = parseInt(targetElement.dataset.stateId || '0')
                    if (activeIssue && stateId) {
                      handleDragEnd({
                        active: {
                          id: activeIssue.id,
                          data: { current: { issue: activeIssue } },
                          rect: { current: { initial: null, translated: null } },
                        },
                        over: {
                          id: stateId,
                          data: { current: { stateId } },
                          rect: { width: 0, height: 0, top: 0, left: 0, bottom: 0, right: 0 },
                          disabled: false,
                        },
                        activatorEvent: e.nativeEvent,
                        delta: { x: 0, y: 0 },
                        collisions: null,
                      } as DragEndEvent)
                    }
                  }}
                >
                  <Column state={state} issues={issuesByState[state.id] || []} />
                </div>
              </SortableContext>
            </div>
          ))}
        </div>

        <DragOverlay>
          {activeIssue ? (
            <div className="rotate-3 scale-105">
              <IssueCard issue={activeIssue} />
            </div>
          ) : null}
        </DragOverlay>
      </DndContext>
    </div>
  )
}
