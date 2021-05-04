from djongo import models

class MaterialType(models.Model):
    typeName = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.typeName

class Material(models.Model):
    materialType = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, blank=False)
    imageLink = models.CharField(max_length=1023, blank=False)