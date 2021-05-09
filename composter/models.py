from djongo import models
from datetime import *

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
    description = models.TextField(max_length=1023, blank=False)
    composter = models.ForeignKey(Composter, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.initDate, self.description)

class Measurement(models.Model):
    _id = models.ObjectIdField()
    composter = models.ForeignKey(Composter, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    co2 = models.FloatField(blank=False)
    ph = models.FloatField(blank=False)
    pressure = models.FloatField(blank=False)
    humidity = models.FloatField(blank=False)
    temperature = models.FloatField(blank=False)
    cn = models.FloatField(blank=False)
    oxigen = models.FloatField(blank=False)
    weight = models.FloatField(blank=False)

    def trigger_alerts(self):
        alert_description = ""

        if self.humidity>0.35:
            alert_description+="Humidade maior que 35%, "

        if self.ph>8.0:
            alert_description+="PH maior que 8.0, "
            
        if self.ph<6.0:
            alert_description+="PH menor que 6.0, "
        
        if self.cn<20:
            alert_description+="Relação Carbono/Nitrogenio menor que 20/1, "

        if self.oxigen>0.6:
            alert_description+="Aeração maior que 60%, "
        
        if self.oxigen<0.1:
            alert_description+="Aeração menor que 10%, "

        if self.temperature<10:
            alert_description+="Temperatura menor que 10°C, "
            
        if self.temperature>80:
            alert_description+="Temperatura maior que 80°C, "

        if alert_description:
            Alert.objects.create(
                alertType=1,
                description=alert_description[:-2],
                composter=self.composter
            )
        else:
            active_alerts = Alert.objects.filter(composter=self.composter, endDate=None, alertType=1)
            for each in active_alerts:
                each.endDate = datetime.now()
                each.save()