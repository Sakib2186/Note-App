from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class UserInfo(models.Model):
    email=models.EmailField(null=False,blank=False)
    username=models.CharField(primary_key=True,null=False,blank=False,max_length=20)
    
    class Meta:
        verbose_name="User Information"
    
    def __str__(self) -> str:
        return self.username

class UserNotes(models.Model):
    title = models.CharField(null=True, blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    description = RichTextField()
    username = models.ForeignKey(UserInfo, null=False, blank=False, on_delete=models.CASCADE)
    note_label = models.CharField(null=True, blank=True, max_length=5000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Notes"

    def __str__(self) -> str:
        return str(self.pk)


class NoteImage(models.Model):
    note = models.ForeignKey(UserNotes, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='UserNotePictures/')

    class Meta:
        verbose_name = "Notes Image"

    def __str__(self) -> str:
        return str(self.pk)
    
class Notes_Label(models.Model):
    labelName = models.CharField(null=False, blank=False, max_length=100)
    label_for = models.ForeignKey(UserInfo, default=None,null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Notes Label"

    def __str__(self) -> str:
        return str(self.labelName)

 
    

