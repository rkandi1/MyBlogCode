from django.contrib import admin
from accounts import models
from django.contrib.auth.admin import User, Group

# Unreistering the custom
admin.site.unregister(User)
admin.site.unregister(Group)

# Registering custom models for admin
admin.site.register(models.UserAccount)
admin.site.register(models.BlogPosts)
