# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# import uuid

# # Create your models here.
# class MyUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, phone, password=None):
#         if not email:
#             raise ValueError("Users must have an email address")
#         if not first_name:
#             raise ValueError("Users must have an first name")
#         if not last_name:
#             raise ValueError("Users must have an last name")
#         if not password:
#             raise ValueError("Users must have an password")
#         if not phone:
#             raise ValueError("Users must have an phone")
#         user = self.model(
#             email = self.normalize_email(email),
#             first_name = first_name,
#             last_name = last_name,
#             user_id = str(uuid.uuid4()),
#             phone = phone
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, password, phone):
#         user = self.create_user(
#             email = self.normalize_email(email),
#             first_name = first_name,
#             last_name = last_name,
#             user_id = str(uuid.uuid4()),
#             phone = phone,
#             password = password
#         )
#         user.is_admin(True)
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     user_id = models.CharField(max_length=255, unique=True, default=str(uuid.uuid4()))
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = MyUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     @property
#     def is_staff(self):
#         return self.is_admin


# class Organisation(models.Model):
#     org_id = models.CharField(max_length=255, unique=True, default=str(uuid.uuid4()))
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     users = models.ManyToManyField(User, related_name='organisations')

























from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not password:
            raise ValueError("Users must have a password")
        if not phone:
            raise ValueError("Users must have a phone number")
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_id=str(uuid.uuid4()),
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, phone):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_id=str(uuid.uuid4()),
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    user_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Organisation(models.Model):
    org_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='organisations')
