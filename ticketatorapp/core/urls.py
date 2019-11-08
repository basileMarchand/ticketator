from django.conf.urls import url
from django.contrib.auth import views as auth_views

# Import some modular views
from .views import (
    index,
    settings,
    company as vcompanies,
    group as vgroup,
    priority as vpriorities,
    queues as vqueues,
    right as vright,
    search as vsearch,
    states as vstates,
    tickets as vtickets,
    users as vusers,
    calendar as vcalendar,
)


urlpatterns = [
    # Dashboard, main screen spotted
    url(r'^$', index, name='home'),

    # Settings & utilities
    url(r'^settings/$', settings, name='tickets-settings'),

    # Auth
    url(r'^login/$', auth_views.LoginView.as_view(template_name="auth/login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    # Users
    url(r'^settings/user/$', vusers.list_users, name='user-list'),
    url(r'^settings/user/create/$', vusers.manage_user, name='user-create'),
    url(r'^settings/user/(?P<user_id>\d+)/$', vusers.manage_user, name='user-edit'),
    url(r'^settings/user/delete/(?P<user_id>\d+)/$', vusers.delete_user, name='user-delete'),
    url(r'^settings/user/set_togglenavbar/$',
        vusers.set_collapsednavbar_jx, name='user-set-collapsednavbar'),

    # Groups
    url(r'^settings/groups/$', vgroup.list_groups, name='group-list'),
    url(r'^settings/groups/create/$', vgroup.manage_group, name='group-create'),
    url(r'^settings/groups/(?P<group_id>\d+)/$', vgroup.manage_group, name='group-edit'),
    url(r'^settings/groups/delete/(?P<group_id>\d+)/$', vgroup.delete_group, name='group-delete'),

    # Rights
    url(r'^settings/rights/$', vright.list_rights, name='right-list'),
    url(r'^settings/rights/create/', vright.manage_right, name='right-create'),
    url(r'^settings/rights/(?P<right_id>\d+)/$', vright.manage_right, name='right-edit'),
    url(r'^settings/rights/delete/(?P<right_id>\d+)/$',
        vright.delete_right, name='right-delete'),

    # States
    url(r'^settings/state/$', vstates.list_state, name='state-list'),
    url(r'^settings/state/create/$', vstates.manage_state, name='state-create'),
    url(r'^settings/state/(?P<state_id>\d+)/$', vstates.manage_state, name='state-edit'),
    url(r'^settings/state/delete/(?P<state_id>\d+)/$', vstates.delete_state, name='state-delete'),

    # Companies
    url(r'^settings/companies/$', vcompanies.list_companies, name='company-list'),
    url(r'^settings/companies/create/$', vcompanies.manage_company, name='company-create'),
    url(r'^settings/companies/(?P<company_id>\d+)/$', vcompanies.manage_company,
        name='company-edit'),
    url(r'^settings/companies/delete/(?P<company_id>\d+)/$', vcompanies.delete_company,
        name='company-delete'),

    # Priorities
    url(r'^settings/priorities/$', vpriorities.list_priorities, name='priority-list'),
    url(r'^settings/priorities/create/$', vpriorities.manage_priority, name='priority-create'),
    url(r'^settings/priorities/(?P<priority_id>\d+)/$', vpriorities.manage_priority,
        name='priority-edit'),
    url(r'^settings/priorities/delete/(?P<priority_id>\d+)/$', vpriorities.delete_priority,
        name='priority-delete'),

    # Queues
    url(r'^settings/queue/$', vqueues.list_queues, name='queue-list'),
    url(r'^settings/queue/create/$', vqueues.manage_queue, name='queue-create'),
    url(r'^settings/queue/(?P<queue_id>\d+)/$', vqueues.manage_queue, name='queue-edit'),
    url(r'^settings/queue/delete/(?P<queue_id>\d+)/$', vqueues.delete_queue, name='queue-delete'),

    # Tickets
    url(r'^tickets/$', vtickets.list_tickets, name='tickets-list'),
    # List tickets filtering state
    url(r'^tickets/state/(?P<state_id>\d+)/$', vtickets.list_tickets_state,
        name='tickets-list-state'),
    # List tickets filtering queue
    url(r'^tickets/queue/(?P<queue_id>\d+)/$', vtickets.list_tickets_queue,
        name='tickets-list-queue'),
    # List tickets filtering label
    url(r'^tickets/labels/(?P<label>\w+)/$', vtickets.list_tickets_label,
        name='tickets-list-label'),
    url(r'^tickets/create/$', vtickets.manage_ticket, name='tickets-create'),
    url(r'^tickets/edit/(?P<ticket_id>\d+)/$', vtickets.manage_ticket, name='tickets-edit'),
    url(r'^tickets/view/(?P<ticket_id>\d+)/$', vtickets.view_ticket, name='tickets-view'),
    url(r'^tickets/delete/(?P<ticket_id>\d+)/$', vtickets.delete_ticket, name='tickets-delete'),

    # Comments post
    url(r'^tickets/add_comment/(?P<ticket_id>\d+)/$',
        vtickets.add_comment_jx, name='tickets-add-comment'),
    url(r'^tickets/get_comments/(?P<ticket_id>\d+)/$',
        vtickets.get_comments_jx, name='tickets-get-comments'),
    url(r'^tickets/del_comment/$', vtickets.del_comment_jx, name='tickets-del-comment'),

    # Post percentage
    url(r'^tickets/set_percentage/(?P<ticket_id>\d+)/range/$',
        vtickets.set_percentage_jx, name='tickets-set-percentage'),
    url(r'^tickets/get_percentage/(?P<ticket_id>\d+)/$',
        vtickets.get_percentage_jx, name='tickets-get-percentage'),

    # Microtask post
    url(r'^tickets/add_microtask/(?P<ticket_id>\d+)/$',
        vtickets.add_microtask_jx, name='tickets-add-microtask'),
    url(r'^tickets/get_microtask/(?P<mk_id>\d+)/$',
        vtickets.get_microtask_jx, name='tickets-get-microtask'),
    url(r'^tickets/get_microtasks/(?P<ticket_id>\d+)/$',
        vtickets.get_microtasks_jx, name='tickets-get-microtasks'),
    url(r'^tickets/del_microtask/$', vtickets.del_microtask_jx, name='tickets-del-microtasks'),

    # Search
    url(r'^search/$', vsearch.search, name='search'),

    # Calendar
    url(r'^calendar/$', vcalendar.view_calendar, name='calendar'),
    url(r'^calendar/get_events/$', vcalendar.get_events, name='get_events'),
]
