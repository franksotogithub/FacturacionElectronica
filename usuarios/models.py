from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from modulos.models import Rol ,Permiso
# Create your models here.

class UserManager (BaseUserManager,models.Manager):

    def _create_user(self, usuario, password, is_staff, is_superuser, is_active=True, **extra_fields):
        user = self.model(usuario=usuario,is_staff=is_staff, is_superuser=is_superuser, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, usuario, password=None,is_active=True, **extra_fields):
        return self._create_user(usuario, password, False,
                                 False, is_active, **extra_fields)

    def create_superuser(self, usuario, password=None, **extra_fields):
        return self._create_user(usuario, password, True,
                                 True, True, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    usuario = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100, blank=True, null=True, default=None)
    dni = models.CharField(max_length=8, blank=True, null=True, default=None)
    email = models.EmailField(max_length=100, blank=True, null=True, default=None)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)
    avatar = models.URLField(max_length=255, blank=True, null=True, default=None)
    rol= models.ForeignKey(Rol,blank=True, null=True, on_delete=False)

    objects = UserManager()
    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'dni']

    def get_short_name(self):
        return self.usuario

    def bienvenida(self):
        return 'Bienvenido: {} {}'.format(self.nombres, self.apellidos)

    def __str__(self):
        return self.usuario