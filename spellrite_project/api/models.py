from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 

class Teacher(AbstractUser):
    """
    Custom Teacher model extending Django's AbstractUser.
    Includes additional fields: organization, class_name, access_code.
    """
    organization = models.CharField(max_length=100)
    class_name   = models.CharField(max_length=100)
    access_code  = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Teachers'  # Maps to the 'Teachers' table in the database
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# api/models.py

class SpellingList(models.Model):
    """
    Model representing a spelling list created by a teacher.
    """
    list_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(
        Teacher,
        related_name='spelling_lists',
        on_delete=models.CASCADE
    )
    list_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Spelling_Lists'  # Maps to the 'Spelling_Lists' table
        ordering = ['list_name']
    
    def __str__(self):
        return self.list_name

class SpellingListWord(models.Model):
    """
    Model representing words in a specific spelling list.
    """
    list_word_id = models.AutoField(primary_key=True)
    spelling_list = models.ForeignKey(
        SpellingList,
        related_name='words',
        on_delete=models.CASCADE
    )
    word = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Spelling_List_Words'  # Maps to the 'Spelling_List_Words' table
        ordering = ['word']
    
    def __str__(self):
        return self.word