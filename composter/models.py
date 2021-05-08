from djongo import models

class MaterialType(models.Model):
    _id = models.ObjectIdField()
    typeName = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.typeName

class Material(models.Model):
    _id = models.ObjectIdField()
    materialType = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, blank=False)
    imageLink = models.CharField(max_length=1023, blank=False)

    def __str__(self):
        return self.name

class Composter(models.Model):
    _id = models.ObjectIdField()
    supermarketId = models.IntegerField()
    macAddress = models.CharField(max_length=18, blank=False)
    name = models.CharField(max_length=127, blank=False)
    description = models.TextField()
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Alert(models.Model):
    _id = models.ObjectIdField()
    alertType = models.IntegerField()
    initDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField()
    description = models.TextField(max_length=255, blank=False)
    composter = models.ForeignKey(Composter, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.initDate, self.description)