
from django.contrib import admin
from livechat.models import User

class UserAdmin(admin.ModelAdmin):
 list_display=('name','email')
    
admin.site.register(User, UserAdmin)