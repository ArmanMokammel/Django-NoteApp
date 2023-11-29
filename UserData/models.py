from django.db import models

# Create your models here.

class UserInfo(models.Model):
    email=models.EmailField(null=False, blank=False)
    username=models.CharField(primary_key=True, null=False, blank=False, max_length=20)

    class Meta:
        verbose_name="User Information"

    def __str__(self) -> str:
        return self.username


class UserNotes(models.Model):
    title=models.CharField(null=True, blank=True, max_length=50)
    description=models.CharField(null=False, blank=False, max_length=500)
    image=models.ImageField(null=True, blank=True, upload_to='UserNotePictures/')
    username=models.ForeignKey(UserInfo, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name="User Notes"

    def __str__(self) -> str:
        return str(self.pk)