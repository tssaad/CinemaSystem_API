from django.db import models

class Movie(models.Model):
    hall   = models.CharField(max_length=10)
    movie  = models.CharField(max_length=10)
    date   = models.DateField(auto_now=True)

    def __str__(self):
        return self.movie

class Guest(models.Model):
    name    = models.CharField(max_length=15)
    phone   = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest   = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="reservation")
    movie   = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reservation")

    def __str__(self):
        return self.guest
