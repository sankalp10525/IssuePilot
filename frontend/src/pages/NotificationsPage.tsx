import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { notificationsApi } from '@/api/notifications'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Bell, Check, CheckCheck, Mail, AlertCircle, GitPullRequest, MessageSquare, UserPlus } from 'lucide-react'
import { useToast } from '@/components/ui/use-toast'
import type { Notification } from '@/api/types'

export default function NotificationsPage() {
  const { toast } = useToast()
  const queryClient = useQueryClient()
  const [filter, setFilter] = useState<'all' | 'unread'>('all')

  const { data: notifications, isLoading } = useQuery({
    queryKey: ['notifications', filter],
    queryFn: () => notificationsApi.list(filter === 'unread' ? false : undefined),
  })

  const { data: unreadCount } = useQuery({
    queryKey: ['notifications-unread-count'],
    queryFn: () => notificationsApi.getUnreadCount(),
    refetchInterval: 30000, // Refetch every 30 seconds
  })

  const markAsReadMutation = useMutation({
    mutationFn: (id: number) => notificationsApi.markAsRead(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] })
      queryClient.invalidateQueries({ queryKey: ['notifications-unread-count'] })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to mark notification as read',
        variant: 'destructive',
      })
    },
  })

  const markAllAsReadMutation = useMutation({
    mutationFn: () => notificationsApi.markAllAsRead(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] })
      queryClient.invalidateQueries({ queryKey: ['notifications-unread-count'] })
      toast({
        title: 'Success',
        description: 'All notifications marked as read',
      })
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to mark all as read',
        variant: 'destructive',
      })
    },
  })

  const getNotificationIcon = (type: string) => {
    const icons: Record<string, JSX.Element> = {
      mention: <MessageSquare className="h-5 w-5 text-blue-500" />,
      assignment: <UserPlus className="h-5 w-5 text-green-500" />,
      comment: <MessageSquare className="h-5 w-5 text-purple-500" />,
      state_change: <GitPullRequest className="h-5 w-5 text-orange-500" />,
      watching: <Bell className="h-5 w-5 text-indigo-500" />,
    }
    return icons[type] || <AlertCircle className="h-5 w-5 text-gray-500" />
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

  const handleNotificationClick = (notification: Notification) => {
    if (!notification.is_read) {
      markAsReadMutation.mutate(notification.id)
    }
  }

  const filteredNotifications = notifications || []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <Bell className="h-8 w-8" />
            Notifications
          </h1>
          <p className="text-muted-foreground mt-1">
            Stay updated with your project activities
          </p>
        </div>
        {unreadCount && unreadCount.count > 0 && (
          <Button
            variant="outline"
            onClick={() => markAllAsReadMutation.mutate()}
            disabled={markAllAsReadMutation.isPending}
            className="gap-2"
          >
            <CheckCheck className="h-4 w-4" />
            Mark all as read
          </Button>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <Bell className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-2xl font-bold">{notifications?.length || 0}</p>
                <p className="text-xs text-muted-foreground">Total notifications</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-100 dark:bg-orange-900/30 rounded-lg">
                <Mail className="h-5 w-5 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <p className="text-2xl font-bold">{unreadCount?.count || 0}</p>
                <p className="text-xs text-muted-foreground">Unread</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
                <Check className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-2xl font-bold">
                  {(notifications?.length || 0) - (unreadCount?.count || 0)}
                </p>
                <p className="text-xs text-muted-foreground">Read</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={filter} onValueChange={(v) => setFilter(v as 'all' | 'unread')}>
        <TabsList>
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="unread">
            Unread
            {unreadCount && unreadCount.count > 0 && (
              <Badge variant="destructive" className="ml-2 px-1.5 py-0 text-xs">
                {unreadCount.count}
              </Badge>
            )}
          </TabsTrigger>
        </TabsList>

        <TabsContent value={filter} className="mt-6">
          {isLoading ? (
            <Card>
              <CardContent className="py-12 text-center text-muted-foreground">
                Loading notifications...
              </CardContent>
            </Card>
          ) : filteredNotifications.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <Bell className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No notifications</h3>
                <p className="text-sm text-muted-foreground">
                  {filter === 'unread'
                    ? "You're all caught up! No unread notifications."
                    : 'You have no notifications yet.'}
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-2">
              {filteredNotifications.map((notification) => {
                const linkTo = notification.issue_key
                  ? `/projects/${notification.project_key?.split('-')[0]}/issues/${notification.issue_key}`
                  : notification.project_key
                  ? `/projects/${notification.project_key}`
                  : undefined

                const NotificationCard = (
                  <Card
                    className={`transition-all duration-200 hover:shadow-md cursor-pointer ${
                      !notification.is_read
                        ? 'bg-blue-50/50 dark:bg-blue-950/20 border-l-4 border-l-blue-500'
                        : 'hover:bg-muted/30 border-l-4 border-l-transparent hover:border-l-primary'
                    }`}
                    onClick={() => handleNotificationClick(notification)}
                  >
                    <CardContent className="p-4">
                      <div className="flex gap-4">
                        <div className="flex-shrink-0 mt-1">
                          {getNotificationIcon(notification.notification_type)}
                        </div>
                        <div className="flex-1 min-w-0 space-y-1">
                          <div className="flex items-start justify-between gap-2">
                            <h4 className="font-semibold text-sm line-clamp-1">
                              {notification.title}
                            </h4>
                            <span className="text-xs text-muted-foreground whitespace-nowrap">
                              {formatTime(notification.created_at)}
                            </span>
                          </div>
                          <p className="text-sm text-muted-foreground line-clamp-2">
                            {notification.message}
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            {!notification.is_read && (
                              <Badge variant="default" className="text-xs">
                                New
                              </Badge>
                            )}
                            {notification.issue_key && (
                              <Badge variant="outline" className="text-xs font-mono">
                                {notification.issue_key}
                              </Badge>
                            )}
                            {notification.project_key && !notification.issue_key && (
                              <Badge variant="outline" className="text-xs">
                                {notification.project_key}
                              </Badge>
                            )}
                          </div>
                        </div>
                        {!notification.is_read && (
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={(e) => {
                              e.stopPropagation()
                              markAsReadMutation.mutate(notification.id)
                            }}
                            className="flex-shrink-0"
                          >
                            <Check className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                )

                return linkTo ? (
                  <Link key={notification.id} to={linkTo}>
                    {NotificationCard}
                  </Link>
                ) : (
                  <div key={notification.id}>{NotificationCard}</div>
                )
              })}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
