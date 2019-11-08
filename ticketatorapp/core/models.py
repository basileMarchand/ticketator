#  -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django.forms import ModelForm
from django.urls import reverse
# Added imports
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
# Extending the Django User's model
from django.contrib.auth.models import AbstractUser

# Logger class


class TimeStampedModelMixin(models.Model):
    """
    Abstract Mixin model to add timestamp
    """
    # Timestamp
    created = models.DateTimeField(u"Date created", auto_now_add=True)
    updated = models.DateTimeField(
        u"Date updated", auto_now=True, db_index=True)

    class Meta:
        abstract = True


# => UserType (OP or simple user)
class UserType(TimeStampedModelMixin):
    status = models.CharField(max_length=20)

    def __unicode__(self):
        return self.status


# Extending base User class
# https://micropyramid.com/blog/how-to-create-custom-user-model-in-django/
class User(AbstractUser):
    status_rel = models.ForeignKey(
        UserType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    avatar = models.FileField(
        upload_to='avatar/',
        null=True,
        blank=True
    )
    rssfeed = models.CharField(
        max_length=400,
        null=True,
        blank=True
    )
    collapsednavbar = models.BooleanField(default=False)

    # If is_superuser comes with NULL value, set it to FALSE
    # (we use a personalized form and if not checked, comes as NULL)
    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.is_superuser = False
        super(User, self).save(*args, **kwargs)


# => Companys
class Company(TimeStampedModelMixin):
    name = models.CharField(max_length=100)
    # More fields will be needed...
    logo = models.FileField(upload_to='logo/')

    # phone = pending
    # address = pending
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name 


# => Queues (ex Departments)
class Queue(TimeStampedModelMixin):
    name = models.CharField(max_length=100)
    shortcode = models.CharField(max_length=10)
    description = models.CharField(max_length=30, null=True, blank=True)
    company_rel = models.ForeignKey(Company, on_delete=models.CASCADE)
    # logo = pending....
    # color  = if needed....

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name 

    def __str__(self):
        return self.name 

# => Groups
# Group's rights
class Rights(TimeStampedModelMixin):
    enabled = models.BooleanField(default=True)
    grp_src = models.ForeignKey(
        Group,
        related_name="src_grp",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )
    queue_dst = models.ForeignKey(
        Queue,
        related_name="dst_queue",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )
    # Permited actions
    can_view = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_comment = models.BooleanField(default=False)

    """'
    Check at database state if registry is created or we can create it:
    If you use the admin, to mantain the non-duplicity of the rules, we make a
    secondary check at time to save the object to the DB.
    Yes, you have 2 querys but this is the unique way to avoid errors if you
    use the admin panel to insert some righths
    """

    def detect_rights_exists(self, grp, queue):
        return_query = {}
        obj_query = Rights.objects.filter(grp_src=grp, queue_dst=queue)
        if obj_query:
            return_query['status'] = True
            return_query['numbers'] = [i.id for i in obj_query]
            return return_query
        else:
            return_query['status'] = False
            return return_query

    # Only for new records (self.pk check)
    def save(self, *args, **kwargs):
        detect_function = self.detect_rights_exists(
            self.grp_src, self.queue_dst)
        if not self.pk and detect_function['status']:
            raise ValidationError(
                "Rule already created: model output " + str(
                    detect_function['numbers']) + "")
        else:
            super(Rights, self).save(*args, **kwargs)


# => States
class State(TimeStampedModelMixin):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150, null=True, blank=True)
    active = models.BooleanField(default=True)
    color = models.CharField(default='008ac6', max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.color.startswith("# "):
            self.color = self.color[1:]
        super(State, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


# => Prioritys
class Priority(TimeStampedModelMixin):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


# => Inventory Servers/PC
class InventoryGroup(TimeStampedModelMixin):
    name = models.CharField(max_length=100)
    company_rel = models.ForeignKey(Company, null=True, on_delete=models.DO_NOTHING)


class Inventory(TimeStampedModelMixin):
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(protocol='ipv4')
    group_rel = models.ForeignKey(InventoryGroup, null=True,on_delete=models.DO_NOTHING)


# => Tickets
class Ticket(TimeStampedModelMixin):
    create_user = models.ForeignKey(
        User,
        related_name="c_user",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )
    subject = models.CharField(max_length=40)
    body = models.TextField(
        null=True,
        blank=True
    )
    assigned_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="a_user",
        on_delete=models.DO_NOTHING
    )
    assigned_queue = models.ForeignKey(
        Queue,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )
    assigned_company = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )
    assigned_state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    assigned_prio = models.ForeignKey(Priority, on_delete=models.DO_NOTHING)
    assigned_inventory = models.ForeignKey(
        Inventory,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    percentage = models.IntegerField(
        default=0,
        blank=True,
        null=True
    )

    labels = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return '%s' % (self.id)

    """Return a empty string to avoid problems in JSON serialization"""
    def str_assigned_user_name(self):
        try:
            assigned_user_data = "" + str(self.assigned_user.first_name) + \
                " " + str(self.assigned_user.last_name) + ""
        except:
            assigned_user_data = ""
        return assigned_user_data

    def str_creator_user_name(self):
        try:
            creator_user_data = "" + str(self.create_user.first_name) + " " + \
                str(self.create_user.last_name) + ""
        except:
            creator_user_data = ""
        return creator_user_data

    def get_label_list(self):
        # Remove possible commas at the begin or end, remove whitespaces and split each label
        cleaned_labels = self.labels.strip(',').replace(' ', '').split(',')
        return cleaned_labels

    def as_json(self):
        return dict(
            id=str(self.id),
            date=str(self.created.strftime('%d-%m-%Y %H:%M')),
            subject_data=str(self.subject.encode('utf8')),
            body_data=str(self.body.encode('utf8')),
            state_data=str(self.assigned_state.name),
            state_data_id=str(self.assigned_state.id),
            state_color_data=str(self.assigned_state.color),
            percentage_data=str(self.percentage),
            queue_shortcode=str(self.assigned_queue.shortcode),
            priority=str(self.assigned_prio),
            create_user=self.str_creator_user_name(),
            assigned_user_data=self.str_assigned_user_name(),
        )

    def events_as_json(self):
        return dict(
            id = str(self.id),
            start = str(self.created.strftime('%Y-%m-%d')),
            title = str(self.subject.encode('utf-8')),
            body = str(self.body.encode('utf-8')),
            state_data = str(self.assigned_state.name),
            url = str(reverse('tickets-view', args=(self.id,)))
        )


# => Attachments
#  Method to store tickets attachments inside folders called with related ticket id
def get_attachment_upload_path(instance, filename):
    return os.path.join("ticket_files/%s" % instance.ticket_rel.id, filename)


class Attachment(TimeStampedModelMixin):

    ticket_rel = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.DO_NOTHING)
    file_name = models.FileField(
        upload_to=get_attachment_upload_path, null=True, blank=True)

    def shortfilename(self):
        return os.path.basename(self.file_name.name)


class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        fields = '__all__'


# => Comments
class Comments(TimeStampedModelMixin):
    ticket_rel = models.ForeignKey(Ticket, related_name='ticket_rel_comm', on_delete=models.DO_NOTHING)
    user_rel = models.ForeignKey(User, related_name='user_rel_comm', on_delete=models.DO_NOTHING)
    comment = models.TextField(null=True, blank=True)
    private = models.BooleanField(default=False)

    """Return this dict to avoid the NO-NESTED objects in serialize library"""

    def as_json(self, request):
        if request.user.id == self.user_rel.id or request.user.is_superuser:
            delete_comment = True
        else:
            delete_comment = False

        return dict(
            human_name="" + self.user_rel.username + "",
            avatar_data=str(self.user_rel.avatar),
            # UTF8 in order to avoid encoding problems
            comment_data=str(self.comment.encode('utf8')),
            id=str(self.id),
            delete_comment=str(delete_comment),
            date_data=str(self.created.strftime('%Y-%m-%d %H:%M')))


class Microtasks(TimeStampedModelMixin):
    ticket_rel = models.ForeignKey(Ticket, related_name='ticket_rel_mtask', on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=40)
    body = models.TextField(null=True, blank=True)
    assigned_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.DO_NOTHING)
    percentage = models.IntegerField(default=0, blank=True, null=True)

    def as_json(self):
        return dict(
            # UTF8 in order to avoid encoding problems
            id=str(self.id),
            subject_data=str(self.subject.encode('utf8')),
            body_data=str(self.body.encode('utf8')),
            state_data=str(self.assigned_state),
            state_data_id=str(self.assigned_state.id),
            state_color_data=str(self.assigned_state.color),
            date_data=str(self.created.strftime('%d/%m/%y %H:%M:%S')),
            percentage_data=int(self.percentage)
        )


class Logs(TimeStampedModelMixin):
    log_ticket = models.ForeignKey(Ticket, related_name='ticket_log', on_delete=models.DO_NOTHING)
    log_user = models.ForeignKey(User, related_name='user_log', on_delete=models.DO_NOTHING)
    log_action = models.CharField(max_length=200)
    log_destiny = models.CharField(max_length=200)
