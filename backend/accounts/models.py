from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.dispatch import receiver
from django.db.models.signals import post_save

from address.models import Address


class UserAccountsManager(BaseUserManager):
    """
    A custom manager for the User model that provides methods for creating different types of users.

    Methods:
        create_user(email, last_name, first_name, password=None, **extra_fields):
            Creates a new user with the given email, last name, first name, and optional password and extra fields.

        create_staff(email, last_name, first_name, password=None, **extra_fields):
            Creates a staff user with the given email, last name, first name, and optional password and extra fields.

        create_superuser(email, last_name, first_name, password=None, **extra_fields):
            Creates a superuser with the given email, last name, first name, and optional password and extra fields.

    """

    def create_user(self, email, last_name, first_name, password=None, **extra_fields):
        """
        Creates a new user with the given email, last name, first name, and optional password and extra fields.

        Parameters:
            self (object): The instance of the class
            email (str): The email address of the user
            last_name (str): The last name of the user
            first_name (str): The first name of the user
            password (str, optional): The password for the user, defaults to None
            **extra_fields (dict): Additional fields for the user

        Returns:
            user (object): The newly created user
        """
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email, last_name=last_name, first_name=first_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, last_name, first_name, password=None, **extra_fields):
        """
        Create a staff user with the given email, last name, first name, and optional password and extra fields.
        Return the created user.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(email, last_name, first_name, password, **extra_fields)

    def create_superuser(
        self, email, last_name, first_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, last_name, first_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserAccountsManager()

    def __str__(self):
        if self.username:
            return self.username
        return self.email


class Admin(models.Model):
    """
    A model representing an admin user. The admin user has superuser permissions.
    The admin user will be given full permissions to all items and will manage orders and customers.

    Attributes:
        user (User): The associated user object for the admin.

    Methods:
        __str__(): Returns a string representation of the admin user.

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.user.username:
            return self.user.username
        return self.user.email


class Staff(models.Model):
    """
    A model representing a staff member. The staff member has staff permissions.
    And will be givin special permissions to assigned items.

    Attributes:
        user (User): The user associated with the staff member.

    Methods:
        __str__(): Returns a string representation of the staff member.

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # assigned_items = models.ManyToManyField(Item)

    def __str__(self):
        if self.user.username:
            return self.user.username
        return self.user.email


class Customer(models.Model):
    """
    A model representing a customer in the system.

    Attributes:
        user (User): The user associated with the customer.
        default_billing_address (Address): The default billing address for the customer.
        default_shipping_address (Address): The default shipping address for the customer.

    Methods:
        __str__(): Returns a string representation of the customer.

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_billing_address = models.ForeignKey(
        Address,
        related_name="billing_customers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    default_shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_customers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.user.username:
            return self.user.username
        return self.user.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_admin(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Admin.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_staff(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        Staff.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        Customer.objects.create(user=instance)


post_save.connect(create_staff, sender=settings.AUTH_USER_MODEL)
post_save.connect(create_customer, sender=settings.AUTH_USER_MODEL)
post_save.connect(create_admin, sender=settings.AUTH_USER_MODEL)
