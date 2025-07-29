from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PlantedTree, Profile, Tree, User, Account

@admin.action(description='ativar multiplas contas')
def activate(modeladmin, request, queryset):
  queryset.update(active=True)

@admin.action(description='desativar multiplas contas')
def inactivate(modeladmin, request, queryset):
  queryset.update(active=False)

class AccountAdmin(admin.ModelAdmin):
  list_display = ('name', 'created', 'active')
  list_editable = ('active',)
  actions = [activate, inactivate]

class PlantedTreeAdmin(admin.ModelAdmin):
  list_display = (
    'tree', 'user', 'account', 'planted_at', 'age', 'latitude', 'longitude'
  )

class PlantedTreeInline(admin.TabularInline):
  model = PlantedTree
  extra = 1

class TreeAdmin(admin.ModelAdmin):
  list_display = ('name', 'scientific_name')
  inlines = [PlantedTreeInline]

class ProfileInline(admin.StackedInline):
  model = Profile
  can_delete = False

class UserAdmin(BaseUserAdmin):
  inlines = (ProfileInline,)

  fieldsets = BaseUserAdmin.fieldsets + (
    ('Accounts', {'fields': ('accounts',)}),
  )

  add_fieldsets = BaseUserAdmin.add_fieldsets + (
    ('Accounts', {'fields': ('accounts',)}),
  )

admin.site.register(Account, AccountAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tree, TreeAdmin)
admin.site.register(PlantedTree, PlantedTreeAdmin)
