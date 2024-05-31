from django.db import models

# Create your models here.

class Account(models.Model):
    connect = models.BooleanField(default=False)
    name = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=20, default='none')
    color = models.CharField(max_length=20, default='none')
    def __list__(self):
        self.accounts = [self.name, self.platform, self.email, self.password, self.created_at, self.tag, self.color]
        return self.accounts

class Content(models.Model):
    Account = models.ForeignKey('Account', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=False)
    icon = models.ImageField(upload_to='images/', default='none')
    image = models.ImageField(upload_to='images/', default='none')
    tag = models.CharField(max_length=20, default='none')
    def __list__(self):
        self.contents = [self.name, self.platform, self.text, self.date, self.icon, self.image, self.tag]
        return self.contents