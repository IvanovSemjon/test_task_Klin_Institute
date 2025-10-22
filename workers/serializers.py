from rest_framework import serializers
from .models import Worker


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id','first_name','middle_name','last_name','position','is_active']


class WorkerDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Worker
        fields = '__all__'
        read_only_fields = ('hired_date','created_by','created_at','updated_at')


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()