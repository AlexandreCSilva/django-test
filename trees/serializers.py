from rest_framework import serializers
from .models import PlantedTree

class PlantedTreeSerializer(serializers.ModelSerializer):
  user = serializers.StringRelatedField()
  tree = serializers.StringRelatedField()
  account = serializers.StringRelatedField()

  class Meta:
    model = PlantedTree
    fields = [
      'id',
      'user',
      'tree',
      'planted_at',
      'account',
      'latitude',
      'longitude'
    ]
