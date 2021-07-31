from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="written_article")
    title = models.TextField()
    sub_title = models.TextField()
    description = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    voted_token_amount = models.FloatField(default=0.0)

    DIRECTION_CHOICES = (("L", "LONG"), ("S", "SHORT"))
    direction_type = models.CharField(
        verbose_name="Long or Short",
        blank=False,
        max_length=2,
        default="L",
        choices=DIRECTION_CHOICES,
    )

    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="voted_article", null=True, blank=True)

    def __str__(self):
        return self.author.username + " - " + self.title


class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="info")
    token_amount = models.FloatField(default=1000.0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username