from rest_framework import serializers
from api.models import Amendment

class AmendmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Amendment
        fields = ['date', 'text', 'title', 'id']