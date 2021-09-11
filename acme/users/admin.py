from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk','user','nombre','username' ,'saldo_inicial',
                        'saldo_final'
                    ]

admin.site.register(Profile, ProfileAdmin)
