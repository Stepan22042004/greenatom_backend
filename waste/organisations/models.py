from django.db import models
from django.contrib.auth.models import AbstractUser


class Capacity(models.Model):
    material = models.CharField(
        max_length=50,
        unique=True
    )


class Storage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacities = models.ManyToManyField(Capacity, through='StorageCapacity')


class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    storages = models.ManyToManyField(
        Storage,
        through='OrganisationStorage'
    )
    capacities = models.ManyToManyField(
        Capacity,
        through='OrganisationCapacity'
    )


class StorageCapacity(models.Model):
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='capacities_storage'
    )
    capacity = models.ForeignKey(Capacity, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True)
    max_volume = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('storage', 'capacity'),
                name='unique_storage_capacities'
            )
        ]



class OrganisationCapacity(models.Model):
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='capacities_organisation'
    )
    capacity = models.ForeignKey(Capacity, on_delete=models.CASCADE)
    amount = models.IntegerField()
    max_volume = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('organisation', 'capacity'),
                name='unique_organisation_capacities'
            )
        ]


class OrganisationStorage(models.Model):
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='storages_organisation')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    distance = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('organisation', 'storage'),
                name='unique_organisation_storages'
            )
        ]


class User(AbstractUser):
    username = models.CharField(
        max_length=20,
        verbose_name='Никнейм',
        unique=True
    )
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта', unique=True)
    organisations = models.ManyToManyField(
        Organisation,
        blank=True,
    )

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
