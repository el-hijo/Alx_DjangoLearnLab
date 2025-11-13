from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)



class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)  # Optional field
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)



# ------------------------------
# 3️⃣ Example Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=13, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

