from django.contrib import admin

from .models import ComponentType, ComponentInstance, Scene


class ComponentTypeAdmin(admin.ModelAdmin):
    pass


class ComponentInstanceAdmin(admin.ModelAdmin):
    pass


class SceneAdmin(admin.ModelAdmin):
    pass


admin.site.register(ComponentType, ComponentTypeAdmin)
admin.site.register(ComponentInstance, ComponentInstanceAdmin)
admin.site.register(Scene, SceneAdmin)
