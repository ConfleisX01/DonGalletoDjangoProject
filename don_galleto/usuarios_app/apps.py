from django.apps import AppConfig

class UsuariosAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios_app"

    def ready(self):
        self.crear_grupos()

    def crear_grupos(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from usuarios_app.models import Usuario 

        grupos_permisos = {
            "administrador": ["add_usuario", "change_usuario", "view_usuario"],
            "usuario": ["view_usuario"],
        }

        content_type = ContentType.objects.get_for_model(Usuario)

        for nombre_grupo, permisos in grupos_permisos.items():
            grupo, creado = Group.objects.get_or_create(name=nombre_grupo)
            permisos_objs = Permission.objects.filter(codename__in=permisos, content_type=content_type)
            grupo.permissions.set(permisos_objs)
