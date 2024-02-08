from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.utils import timezone
from datetime import timedelta
from django_countries.fields import CountryField

# Create your models here.
class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)


    def __str__(self):
        return f"{self.name} ({self.phone_number})"
    
    def get_owner(self):
        matching_users = User.objects.get(phone_number=self.phone_number)
        return matching_users or None


class NullableUniqueEmailField(models.EmailField):
    def get_prep_value(self, value):
        return value if value != "" else None
    
class UserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number is required')
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    email = NullableUniqueEmailField(max_length=255, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    contacts = models.ManyToManyField(Contact, related_name='users')
    registration_date = models.DateTimeField(auto_now=True)
    country = CountryField(blank_label="(select country)", default="FR")
    route_clustering_begins = models.BooleanField(default=False) # the clustering of the routes have already start


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.phone_number
    
    def get_extended_contacts(self):
        """
        Récupère une liste des contacts de l'utilisateur, ainsi que des contacts des contacts.
        Évite les doublons et exclut les contacts sans utilisateur associé.
        """
        processed_users = set()  # Pour garder une trace des utilisateurs déjà traités
        contacts_to_process = [self]  # Commence par l'utilisateur lui-même
        all_contacts = set()  # Pour stocker tous les contacts uniques

        while contacts_to_process:
            current_user = contacts_to_process.pop()
            if current_user.id in processed_users:
                continue  # Skip si cet utilisateur a déjà été traité

            for contact in current_user.contacts.all():
                all_contacts.add(contact)
                owner = contact.get_owner()
                if owner and owner.id not in processed_users:
                    contacts_to_process.append(owner)

            processed_users.add(current_user.id)

        return list(all_contacts)
    
    def get_user_clusters(self):
        # Récupère toutes les routes de cet utilisateur
        routes = self.route.all()
        # Récupère les clusters associés à ces routes
        clusters = set(route.cluster for route in routes if route.cluster)
        return clusters



class Riddle(models.Model):
    """ex : je suis un animal qui fait miaou → possibilitées : chat, chien, ornithorynque """
    question = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=25)
    
    def __str__(self):
        return f"{self.correct_answer}"
    
    
class RiddleToken(models.Model):
    token = models.CharField(max_length=64, unique=True)  # Assurez-vous que la longueur est appropriée
    riddle = models.ForeignKey(Riddle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        time_diff = timezone.now() - self.created_at
        age_minutes = time_diff.total_seconds() / 60
        return f"{age_minutes:.2f} min"
    
    def is_valid(self):
        now = timezone.now()
        time_diff = now - self.created_at
        if time_diff >= timedelta(minutes=10):
            self.delete()  # Supprime le token s'il est expiré
            return False
        return True
