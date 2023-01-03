from rest_framework import serializers
from .models import Customer, Course, HomeWork,WorkApprove


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'status']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = '__all__'


class WorkApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkApprove
        fields = ['id', 'approve']
