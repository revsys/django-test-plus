from django.db import models


class Data(models.Model):
    """ Simple model to test our query assertions """
    name = models.CharField(max_length=50)
