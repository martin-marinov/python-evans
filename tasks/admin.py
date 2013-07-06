from django.contrib import admin


from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_points', 'closes_at_pretty')

    def closes_at_pretty(self, obj):
        return obj.closes_at.strftime('%d.%m.%Y, %a, %H:%M')

    closes_at_pretty.short_description = 'Closes at'

admin.site.register(Task, TaskAdmin)
