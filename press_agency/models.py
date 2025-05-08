from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True, null=True, help_text="A brief description of the topic"
    )
    owner = models.ForeignKey(
        "Redactor", on_delete=models.CASCADE, related_name="topics"
    )

    def number_publications_in_a_topic(self):
        return self

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(blank=True, null=True)
    pen_name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    autobiography = models.TextField(blank=True, null=True)

    def number_of_publications(self):
        return self.newspaper_set.count()

    class Meta:
        verbose_name = "Redactor"
        verbose_name_plural = "Redactors"

    def __str__(self):
        return self.username


class Newspaper(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(unique=True)
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Redactor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, {self.content}"
