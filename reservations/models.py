from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

    def __str__(self):
        return self.title


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    hall = models.CharField(max_length=50)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"


class Reservation(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.screening}"