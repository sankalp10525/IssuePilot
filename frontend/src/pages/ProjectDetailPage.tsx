import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { projectsApi } from '@/api/projects'
import { issuesApi } from '@/api/issues'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function ProjectDetailPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const id = parseInt(projectId!)

  const { data: project, isLoading: projectLoading } = useQuery({
    queryKey: ['project', id],
    queryFn: () => projectsApi.get(id),
  })

  const { data: issues, isLoading: issuesLoading } = useQuery({
    queryKey: ['issues', id],
    queryFn: () => issuesApi.list(id),
  })

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
            <Button size="sm">Create Issue</Button>
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
