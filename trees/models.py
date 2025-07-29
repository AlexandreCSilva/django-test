from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
  name = models.CharField(unique=True)
  created = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(default=True)
  
  def __str__(self):
    return self.name
  
class User(AbstractUser):
  accounts = models.ManyToManyField(Account, related_name='users', blank=True)

  def plant_tree(self, tree, location, account):
    lat, lon = location
    PlantedTree.objects.create(
      user=self,
      tree=tree,
      account=account,
      latitude=lat,
      longitude=lon
    )

  def plant_trees(self, plants):
    planted_trees = []
    for tree, location, account in plants:
      lat, lon = location
      planted_trees.append(
        PlantedTree(
          user=self,
          tree=tree,
          account=account,
          latitude=lat,
          longitude=lon
        )
      )
    PlantedTree.objects.bulk_create(planted_trees)

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  about = models.TextField(blank=True)
  joined = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.user.username

class Tree(models.Model):
  name = models.CharField(max_length=100)
  scientific_name = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.name

class PlantedTree(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planted_trees')
  tree = models.ForeignKey(Tree, on_delete=models.PROTECT, related_name='times_planted')
  account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='planted_trees')
  planted_at = models.DateTimeField(auto_now_add=True)
  age = models.IntegerField(null=True, blank=True)
  latitude = models.DecimalField(max_digits=9, decimal_places=2)
  longitude = models.DecimalField(max_digits=9, decimal_places=2)

  def __str__(self):
    return f'{self.tree.name} plantada por {self.user.username} na conta {self.account.name}'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()