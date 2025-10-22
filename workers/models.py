from django.db import models
from django.conf import settings


class Worker(models.Model):
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    middle_name = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Отчество"
    )
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Электронная почта"
    )
    position = models.CharField(max_length=200, verbose_name="Должность")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    hired_date = models.DateField(auto_now_add=True, verbose_name="Дата приёма")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_workers",
        verbose_name="Создатель записи",
    )
    # Тут будут технические данные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["position"]),
            models.Index(fields=["is_active"]),
        ]
        ordering = ["created_at"]
