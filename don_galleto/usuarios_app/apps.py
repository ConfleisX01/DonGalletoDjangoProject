from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

class UsuariosAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios_app"

    def ready(self):
        try:
            self.crear_grupos()
        except (OperationalError, ProgrammingError):
            # 🔹 Evita ejecutar esto si la base de datos aún no está lista
            print("Base de datos no lista. Grupos no creados.")
    
    def crear_grupos(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from usuarios_app.models import Usuario

        grupos_permisos = {
            "administrador": [
                #Usuarios
                "add_usuario",
                "change_usuario",
                "view_usuario",

                #Dashboard
                "view_dashboard",
                
                #recetas
                'add_recetas',
                'change_recetas',
                'view_recetas',
                
                #inventario
                ],
            
            "usuario": ["view_usuario"],
            "cliente": ["view_carrito", "buy_galletas"]
        }

        try:
            content_type = ContentType.objects.get_for_model(Usuario)
            for nombre_grupo, permisos in grupos_permisos.items():
                grupo, creado = Group.objects.get_or_create(name=nombre_grupo)
                permisos_objs = Permission.objects.filter(codename__in=permisos, content_type=content_type)
                grupo.permissions.set(permisos_objs)
        except Exception as e:
            print(f"Error al crear grupos: {e}")
