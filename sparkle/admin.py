from django.contrib import admin
from sparkle.models import Application, Version, SystemProfileReport, SystemProfileReportRecord
from notifications.models import Subscriber, Group, Notification, Toggle
from django import forms
from django.contrib.auth.models import User
from notifications.views import send_notifications
from django.conf.urls import url
from django.http import HttpResponse, HttpResponseRedirect
import json

class ApplicationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(Application, ApplicationAdmin)


class NotificationForm(forms.ModelForm):
    subscribers = forms.ModelMultipleChoiceField (queryset=Subscriber.objects.all(), required=False)
    groups = forms.ModelMultipleChoiceField (queryset=Group.objects.all(), required=False)
    send_now = forms.BooleanField(required=False, initial=True)
    

class VersionAdmin(admin.ModelAdmin):
    form = NotificationForm

    list_display = ('title', 'version', 'short_version', 'application', 'publish_date', 'mandatory', )
    list_display_links = list_display
    list_filter = ('application', 'publish_date',)
    fieldsets = (
        (None, {'fields': ('application', 'title', 'release_notes', 'version', 'short_version', 'update', 'publish_date', 'mandatory', )}),
        ('Details', {'fields': ('dsa_signature', 'length', 'minimum_system_version', 'created',), 'classes': ('collapse',)}),
        ('Notifications', {'fields': ('subscribers', 'groups','send_now'), 'classes': ('collapse',)}),
        
    )
    readonly_fields = ('created', )
    ordering = ('-publish_date', )

    def get_urls(self):
        urls = super(VersionAdmin, self).get_urls()
        my_urls = [
            url(r'^get-groups/$', self.get_groups),
        ]
        return my_urls + urls

    def save_model(self, request, obj, form, change): 
        subscribers = form.cleaned_data.get('subscribers', None)
        groups = form.cleaned_data.get('groups', None)
        send_now = form.cleaned_data.get('send_now', None)
        # ...do something
       
        instance = form.save(commit=False)
        instance.save()
        print instance.application
        notification = Notification.objects.update_or_create(version=instance, user = User.objects.get(id=int(request.user.id)), app_name = str(instance.application))[0]

        email_list = []


        for subscriber in subscribers:
            notification.subscribers.add(subscriber)
            if subscriber.email not in email_list:
                email_list.append(subscriber.email)

        for gr in groups:
            notification.groups.add(gr)
            for sub in gr.subscribers.all():
                if sub.email not in email_list:
                    email_list.append(sub.email)

        if send_now:
            # t = Toggle.objects.get_or_create(id=1)[0]
            # if t.toggle:
            send_notifications(notification, email_list)

        return instance

    class Media:
        js = ['/static/js/get_groups.js']

    def get_groups(self, request):


        app = Application.objects.get(id=int(request.GET.get('id', None)))
        notification = Notification.objects.filter(app_name = app.name).last()
        groups = []
        if notification:
            for g in notification.groups.all():
                groups.append(g.id)

        return HttpResponse(json.dumps(groups), content_type="application/json")


admin.site.register(Version, VersionAdmin)

class SystemProfileReportRecordInline(admin.TabularInline):
    model = SystemProfileReportRecord
    extra = 0
    max_num = 0
    readonly_fields = ('key', 'value')
    can_delete = False

class SystemProfileReportAdmin(admin.ModelAdmin):
    inlines = [SystemProfileReportRecordInline,]

admin.site.register(SystemProfileReport, SystemProfileReportAdmin)

class SystemProfileReportRecordAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    list_filter = ('key',)

admin.site.register(SystemProfileReportRecord, SystemProfileReportRecordAdmin)

