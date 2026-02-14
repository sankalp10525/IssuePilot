import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { issuesApi } from '@/api/issues'
import { projectsApi } from '@/api/projects'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Search, Filter } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function SearchPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedProject, setSelectedProject] = useState<string>('all')
  const [selectedType, setSelectedType] = useState<string>('all')
  const [selectedPriority, setSelectedPriority] = useState<string>('all')
  const [selectedState, setSelectedState] = useState<string>('all')

  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectsApi.list(),
  })

  // Get all issues from all projects for search
  const projectIds = projects?.map((p) => p.id) || []
  
  const issueQueries = useQuery({
    queryKey: ['all-issues', projectIds],
    queryFn: async () => {
      if (projectIds.length === 0) return []
      const allIssuesWithProject = await Promise.all(
        projectIds.map(async (projectId) => {
          const issues = await issuesApi.list(projectId)
          // Add project_id to each issue
          return issues.map((issue) => ({ ...issue, project_id: projectId }))
        })
      )
      return allIssuesWithProject.flat()
    },
    enabled: projectIds.length > 0,
  })

  const issues = issueQueries.data || []

  // Filter issues based on search and filters
  const filteredIssues = issues.filter((issue) => {
    const matchesSearch =
      searchQuery === '' ||
      issue.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      issue.key.toLowerCase().includes(searchQuery.toLowerCase()) ||
      issue.description?.toLowerCase().includes(searchQuery.toLowerCase())

    const matchesProject =
      selectedProject === 'all' || (issue as any).project_id === parseInt(selectedProject)

    const matchesType = selectedType === 'all' || issue.issue_type === selectedType

    const matchesPriority =
      selectedPriority === 'all' || issue.priority === selectedPriority

    const matchesState =
      selectedState === 'all' || issue.state.category === selectedState

    return matchesSearch && matchesProject && matchesType && matchesPriority && matchesState
  })

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      highest: 'destructive',
      high: 'destructive',
      medium: 'default',
      low: 'secondary',
      lowest: 'outline',
    }
    return colors[priority] || 'default'
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

  const handleReset = () => {
    setSearchQuery('')
    setSelectedProject('all')
    setSelectedType('all')
    setSelectedPriority('all')
    setSelectedState('all')
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Search Issues</h1>
        <p className="text-muted-foreground">Find issues across all your projects</p>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search by title, key, or description..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-9 h-11"
        />
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-3">
            <Filter className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm font-medium">Filters</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">Project</label>
              <Select value={selectedProject} onValueChange={setSelectedProject}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Projects</SelectItem>
                  {projects?.map((project) => (
                    <SelectItem key={project.id} value={project.id.toString()}>
                      {project.icon} {project.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">Type</label>
              <Select value={selectedType} onValueChange={setSelectedType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="task">Task</SelectItem>
                  <SelectItem value="bug">Bug</SelectItem>
                  <SelectItem value="story">Story</SelectItem>
                  <SelectItem value="epic">Epic</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">Priority</label>
              <Select value={selectedPriority} onValueChange={setSelectedPriority}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Priorities</SelectItem>
                  <SelectItem value="highest">Highest</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="lowest">Lowest</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">Status</label>
              <Select value={selectedState} onValueChange={setSelectedState}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value="todo">To Do</SelectItem>
                  <SelectItem value="in_progress">In Progress</SelectItem>
                  <SelectItem value="done">Done</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          {(searchQuery || selectedProject !== 'all' || selectedType !== 'all' || 
            selectedPriority !== 'all' || selectedState !== 'all') && (
            <div className="mt-4">
              <Button variant="outline" size="sm" onClick={handleReset}>
                Clear All Filters
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Results */}
      <div>
        <div className="mb-4">
          <p className="text-sm text-muted-foreground">
            {filteredIssues.length} {filteredIssues.length === 1 ? 'issue' : 'issues'} found
          </p>
        </div>

        {issueQueries.isLoading ? (
          <div className="text-center py-12 text-muted-foreground">Loading issues...</div>
        ) : filteredIssues.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center text-muted-foreground">
              No issues found matching your search criteria
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-2">
            {filteredIssues.map((issue) => {
              const issueWithProject = issue as any
              const project = projects?.find((p) => p.id === issueWithProject.project_id)
              return (
                <Link
                  key={issue.id}
                  to={`/projects/${issueWithProject.project_id}/issues/${issue.key}`}
                  className="group"
                >
                  <Card className="hover:bg-muted/30 hover:shadow-md transition-all duration-200 cursor-pointer border-l-4 border-l-transparent hover:border-l-primary">
                    <CardContent className="p-4">
                      <div className="flex items-start gap-4">
                        <span className="text-2xl">{getTypeIcon(issue.issue_type)}</span>
                        <div className="flex-1 min-w-0 space-y-2">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="font-mono text-xs text-muted-foreground bg-muted px-2 py-1 rounded group-hover:bg-primary/10 transition-colors">
                              {issue.key}
                            </span>
                            {project && (
                              <span className="text-xs text-muted-foreground">
                                {project.icon} {project.name}
                              </span>
                            )}
                          </div>
                          <h3 className="font-medium line-clamp-1 group-hover:text-primary transition-colors">
                            {issue.title}
                          </h3>
                          {issue.description && (
                            <p className="text-sm text-muted-foreground line-clamp-2">
                              {issue.description}
                            </p>
                          )}
                          <div className="flex items-center gap-2 flex-wrap">
                            <Badge variant={getPriorityColor(issue.priority) as any} className="capitalize">
                              {issue.priority}
                            </Badge>
                            <Badge variant="outline" className="capitalize">
                              {issue.state.name}
                            </Badge>
                            {issue.assignee && (
                              <span className="text-xs text-muted-foreground">
                                @{issue.assignee.username}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
