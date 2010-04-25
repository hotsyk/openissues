# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import StrAndUnicode, force_unicode
from django.contrib.auth.models import User

from todo.models import *
from todo.templatetags.todo_extras import username


class OpentodoModelForm(ModelForm):
    class Media:
        css = {'all': ('forms.css', )}
        js = ('jquery.formvalidation.1.1.5.js',)


class ProjectForm(OpentodoModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        user_choices = []
        user_list = User.objects.order_by('first_name', 'last_name')
        for item in user_list:
            user_choices.append((item.id, username(item)))
        self.fields['users'].choices = user_choices

    title = forms.CharField()

    class Meta:
        model = Project
        fields = ('title', 'info', 'users')

class ComplexityRadioFieldRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        return mark_safe(u'&nbsp;'.join([u'%s'
                % force_unicode(w) for w in self]))    

class TaskForm(OpentodoModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.available_for(user)

    title = forms.CharField()
    complexity = forms.ChoiceField(widget=forms.RadioSelect(\
                                   renderer=ComplexityRadioFieldRenderer), 
                                   choices=[[0,'0'], [1,'1'], 
                                            [2,'2'], [3,'3'], 
                                            [4,'4'], ])
    
    class Meta:
        model = Task
        fields = ('project', 'title', 'info', 'deadline', 'complexity', 
                 )

    class Media:
        css = {'all': ('ui.datepicker.css', )}
        js = ('ui.datepicker.js', )


class ProjectAttachForm(OpentodoModelForm):
    class Meta:
        model = ProjectAttach
        fields = ('attached_file', )


class TaskAttachForm(OpentodoModelForm):
    class Meta:
        model = TaskAttach
        fields = ('attached_file', )
