from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.constant import FIRST_NAME_LENGTH, LAST_NAME_LENGTH


class Person(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatar/',
        null=True,
        default=None,
        verbose_name='Аватар'
    )
    is_subscribed = models.BooleanField(
        default=False)
    first_name = models.CharField(
        _("first name"),
        max_length=FIRST_NAME_LENGTH,
        blank=False)
    last_name = models.CharField(
        _("last name"),
        max_length=LAST_NAME_LENGTH,
        blank=False)

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',
                       'first_name',
                       'last_name']

    class Meta:
        ordering = ['email']
        verbose_name = 'пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Follower(models.Model):
    user_id = models.ForeignKey(Person,
                                on_delete=models.CASCADE,
                                related_name='following',
                                verbose_name='Подписчик')
    following_id = models.ForeignKey(Person,
                                     on_delete=models.CASCADE,
                                     related_name='followers',
                                     verbose_name='Автор')

    class Meta:
        ordering = ['user_id']
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписка'

    def __str__(self):
        return f'{self.user_id} подписан на {self.following_id}'
