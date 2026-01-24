from django.db import models

# Create your models here.

class Program(models.Model):
    id = models.IntegerField(primary_key = True) # import uuid uuid.uuid4 
    name = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.name}"
    
    # def save(self):
        