from django.db import models

# Create your models here.


class CardDetail(models.Model):
    CARD_TYPE_CHOICES = [
        ('Aadhaar', 'Aadhaar'),
        ('PAN', 'PAN'),
    ]

    card_type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return f"{self.card_type} - {self.name}"

class images(models.Model):

    image = models.ImageField(upload_to='card_images/')
    


    