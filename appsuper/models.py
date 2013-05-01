from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10, unique=True)
    updatetime = models.DateTimeField(auto_now=True)

class Superlative(models.Model):
    owner = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=255, blank=True)
    numfields = models.IntegerField(default=1)
    updatetime = models.DateTimeField(auto_now=True)
    def toDict(self, uname):
        return {'id':self.pk,
                'ownedByMe':self.owner.name == uname,
                'name':self.name,
                'numfields':self.numfields,
                }

class Selection(models.Model):
    user = models.ForeignKey(User)
    superlative = models.ForeignKey(Superlative)
    selection = models.CharField(max_length=25, blank=True)
    index = models.IntegerField(default=1)
    updatetime = models.DateTimeField(auto_now=True)
    def toDict(self):
        return {'id':self.superlative.pk,
                'selection':self.selection, 
                'index':self.index}
        
