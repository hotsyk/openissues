# -*- coding: utf-8 -*-
#------------------------------------------------------------
# openissues (C) 2010 Volodymyr Hotsyk <openissues@hotsyk.com>
# opentodo (c) 2009 Mikhail Grigoriev <mgrigoriev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.core.mail import EmailMessage

TASK_NOTIF_SUBJECTS = {
    1: 'New task',
    2: 'Task was accepted',
    3: 'Task marked as done',
    4: 'Result of task has been approved',
    5: 'Task was reopened'
}

def uniqs(seq):
    return dict(zip(seq, [None,]*len(seq))).keys()

def send_emails(subject, message, recipient_list):
    msg = EmailMessage(subject, message, settings.EMAIL_ADDRESS_FROM, 
                       recipient_list)
    msg.content_subtype = "html"
    msg.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)

# Генерирует upload path для FileField
def make_upload_path(instance, filename):
    upload_path = "uploads"
    if isinstance(instance, ProjectAttach):
        project_id = instance.project.id
        return u"%s/%s/%s" % (upload_path, project_id, filename)

    elif isinstance(instance, TaskAttach):
        project_id = instance.task.project.id
        return u"%s/%s/tasks/%s" % (upload_path, project_id, filename)

# Пользователи в проектах
def users_in_projects(projects):
    users = User.objects.filter(
            Q(avail_projects__in=projects) |\
             Q(is_superuser=True)).distinct().order_by('first_name', 
                                                       'last_name')
    return users


class ProjectManager(models.Manager):
    def available_for(self, user):
        if user.is_superuser:
            return self.all().order_by('title')
        else:
            return user.avail_projects.all().order_by('title')     

class Project(models.Model):
    title = models.CharField("Project", max_length=255)
    info = models.TextField("Description", null=True, blank=True)
    created_at = models.DateTimeField("Date of adding", auto_now_add=True)
    author = models.ForeignKey(User, null=True, db_column='author', 
                               related_name="projects", verbose_name="Author")
    users = models.ManyToManyField(User, blank=True, null=True, 
                                   verbose_name="Team", 
                                   related_name="avail_projects")
    
    objects = ProjectManager()

    def __unicode__(self):
        return self.title
    def _get_tasks_count(self):
        return self.related_tasks.count()
    def _get_tasks_count_active(self):
        return self.related_tasks.exclude(status=3).exclude(status=4).count()
    tasks_count = property(_get_tasks_count)
    tasks_active_count = property(_get_tasks_count_active)

    def is_avail(self, user):
        if user.is_superuser:
            return True
        try:
            user.avail_projects.get(pk=self.pk)
            return True
        except Project.DoesNotExist:
            return False

    def allowed_users(self):
        pass

    def save(self):
        is_new = self._get_pk_val() is None
        super(Project, self).save()
        if is_new:
            self.users.add(self.author)

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"


class ProjectEstimate(models.Model):
    project = models.ForeignKey(Project)
    created_at = models.DateTimeField()
    author = models.ForeignKey(User)
    complexity = models.IntegerField(default=0)
    
    
class Status(models.Model):
    title = models.CharField("Status", max_length=50)
    def __unicode__(self):
        return self.title


class Task(models.Model):
    TASK_TYPES = (
                  (1, 'Task'),
                  (2, 'Defect'),
                  (3, 'Enhancement'),
                  (4, 'Technical debt'),
                  (5, 'Issue'),
                  )
    project = models.ForeignKey(Project, verbose_name="Project", 
                                related_name="related_tasks")
    status = models.ForeignKey(Status, default=1, 
                               verbose_name="Status")
    author = models.ForeignKey(User, null=True, db_column='author', 
                               related_name="tasks", verbose_name="Автор")
    assigned_to = models.ForeignKey(User, null=True, db_column='assigned_to', 
                                    related_name="assigned_tasks", 
                                    verbose_name="Ответственный")
    created_at = models.DateTimeField("Creation date", 
                                      auto_now_add=True)
    title =  models.CharField("Task", max_length=255)
    info = models.TextField("Description", null=True, blank=True)
    deadline = models.DateField("Deadline", null=True, blank=True)
    has_deadline = models.BooleanField(default=0)
    type = models.SmallIntegerField(choices=TASK_TYPES, default=1)
    complexity = models.IntegerField(default=0)
    gitrevision = models.CharField(max_length=255, blank=True, null=True)
    
    
    def __unicode__(self):
        return self.title

    # Уведомления по e-mail (о добавлении задачи, изменении статуса)
    def mail_notify(self, host='', reopened=False):
        if settings.SEND_EMAILS:
            tmpl = get_template('todo/mail/task.html')
            msg_body = tmpl.render( Context({'t':self, 'host':host}) )
            addr = ''
            if reopened:
                notif_id = 5
            else:
                notif_id = self.status.id

            if ( notif_id in (1,4,5) ) and self.assigned_to.email:
                addr = self.assigned_to.email
            elif self.author.email:
                addr = self.author.email
        
            if addr:
                send_emails('[openissues] '+TASK_NOTIF_SUBJECTS[notif_id], 
                            msg_body, [addr])
        
# Комментарии к задачам
class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comments")
    author = models.ForeignKey(User)
    message = models.TextField("Комментарий")
    created_at = models.DateTimeField("Дата", auto_now_add=True)
    reply_to = models.ForeignKey('self', null=True, blank=True)
    class Meta:
        ordering = ['created_at']

    # Уведомление по e-mail о добавлении комментария
    def mail_notify(self, host=''):
        if settings.SEND_EMAILS:
            tmpl = get_template('todo/mail/comment.html')
            msg_body = tmpl.render( Context({'t':self.task, 
                                             'c':self, 'host':host}) )
            addrs = []
            if self.task.author.email:
                addrs.append(self.task.author.email)
            if self.task.assigned_to and self.task.assigned_to.email:
                addrs.append(self.task.assigned_to.email)
            if self.reply_to and self.reply_to.author.email:
                addrs.append(self.reply_to.author.email)
            if addrs:
                send_emails('[openissues] Comment to the task', 
                            msg_body, uniqs(addrs))

# Абстрактный класс для файлов-вложений
class CommonAttach(models.Model):
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    attached_file = models.FileField(upload_to=make_upload_path)
    class Meta:
        abstract=True

# Аттачи к проектам
class ProjectAttach(CommonAttach):
    project = models.ForeignKey(Project, related_name="files")

# Аттачи к задачам
class TaskAttach(CommonAttach):
    task = models.ForeignKey(Task, related_name="files")

    # Уведомление по e-mail о прикреплении файла к задаче
    def mail_notify(self, host=''):
        if settings.SEND_EMAILS:
            tmpl = get_template('todo/mail/file.html')
            msg_body = tmpl.render( Context({'t':self.task, 
                                             'a':self, 'host':host}) )
            addrs = []
            if self.task.author.email:
                addrs.append(self.task.author.email)
            if self.task.assigned_to and self.task.assigned_to.email:
                addrs.append(self.task.assigned_to.email)
            
            if addrs:
                send_emails('[openissues] File was attached to the task', 
                            msg_body, uniqs(addrs))