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
    description=models.TextField()
    username=models.ForeignKey(UserInfo, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name="User Notes"

    def __str__(self) -> str:
        return str(self.pk)
    
class ImageFile(models.Model):
    image=models.ImageField(null=True, blank=True, upload_to='UserNotePictures/')
    user_note=models.ForeignKey(UserNotes, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name="User Note Images"

    def __str__(self) -> str:
        return str(self.pk)
    
    