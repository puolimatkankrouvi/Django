from __future__ import unicode_literals

from django.db import models

#class Band(models.Model):
    #name = models.CharField(max_length=50)
    #def __str__(self):
        #return self.name

class Review(models.Model):
    band_name = models.CharField(max_length=50)#ForeignKey(Band, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=50)
    review_text = models.CharField(max_length=500)

    def __init__(self,b_name,album,review_text):
        self.band_name = b_name
        self.album_title = album
        self.review_text = review_text

    def __str__(self):
        return self.band_name

    class Meta:
        app_label = 'reviews'