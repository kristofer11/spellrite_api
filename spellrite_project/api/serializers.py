# # api/serializers.py

# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class TeacherDetailSerializer(serializers.ModelSerializer):
#     """
#     Serializer for detailed Teacher information.
#     Excludes sensitive fields.
#     """
#     class Meta:
#         model = User
#         # Exclude fields like password, last_login, etc.
#         exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions')

# api/serializers.py

from rest_framework import serializers
from rest_framework.validators import UniqueValidator  
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator # Correct import for validators
from .models import SpellingList, SpellingListWord  # Import your models

User = get_user_model()

class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Teacher instances.
    Handles password hashing and validation.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[MinLengthValidator(8)]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[MinLengthValidator(8)]
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'password2',
            'first_name', 'last_name', 'email',
            'organization', 'class_name', 'access_code',
            'is_staff', 'is_active'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'organization': {'required': True},
            'class_name': {'required': True},
            'access_code': {'required': True},
        }

    def validate(self, attrs):
        """
        Ensure that both password fields match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new Teacher instance with a hashed password.
        """
        validated_data.pop('password2')  # Remove password2 as it's not needed for creation
        password = validated_data.pop('password')
        teacher = User(**validated_data)
        teacher.set_password(password)  # Hash the password
        teacher.save()
        return teacher

    def update(self, instance, validated_data):
        """
        Update an existing Teacher instance.
        Handle password hashing if password is provided.
        """
        validated_data.pop('password2', None)  # Remove password2 if present
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # Hash the new password

        instance.save()
        return instance

class TeacherDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Teacher information.
    Excludes sensitive fields.
    """
    class Meta:
        model = User
        # Exclude fields like password, last_login, etc.
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions')

class SpellingListWordSerializer(serializers.ModelSerializer):
    """
    Serializer for SpellingListWord model.
    """
    class Meta:
        model = SpellingListWord
        fields = '__all__'
        read_only_fields = ['list_word_id', 'created_at', 'updated_at']
        
class SpellingListSerializer(serializers.ModelSerializer):
    words = SpellingListWordSerializer(many=True, read_only=True)

    class Meta:
        model = SpellingList
        # Remove 'teacher' from fields or mark as read-only
        fields = ['list_id', 'list_name', 'created_at', 'updated_at', 'words']
        read_only_fields = ['list_id', 'created_at', 'updated_at', 'words']
        # Alternatively, if you want to include teacher in the representation but not require it during input:
        # fields = ['list_id', 'list_name', 'teacher', 'created_at', 'updated_at', 'words']
        # read_only_fields = ['list_id', 'teacher', 'created_at', 'updated_at', 'words']


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new Teacher.
    """
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[MinLengthValidator(8)]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[MinLengthValidator(8)]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'first_name',
            'last_name',
            'email',
            'organization',
            'class_name',
            'access_code',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'organization': {'required': True},
            'class_name': {'required': True},
            'access_code': {'required': True},
        }

    def validate(self, attrs):
        """
        Ensure that both password fields match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new Teacher instance with a hashed password.
        """
        validated_data.pop('password2')  # Remove password2 as it's not needed for creation
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user