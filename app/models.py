from django.db import models
# Create your models here.

class Student(models.Model):
    studentId = models.CharField(db_column='studentId', primary_key=True, max_length=12)  # Field name made lowercase.
    studentName = models.CharField(db_column='studentName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1, blank=True, null=True)
    telephone = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    studentType = models.CharField(db_column='studentType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idNo = models.CharField(db_column='idNo', max_length=18, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=50, blank=True, null=True)
    schoolYear = models.DateField(db_column='schoolYear', blank=True, null=True)  # Field name made lowercase.
    avatarUrl = models.CharField(db_column='avatarUrl', max_length=4000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student'


class Student1(models.Model):
    studentid = models.CharField(db_column='studentId', primary_key=True, max_length=12)  # Field name made lowercase.
    studentname = models.CharField(db_column='studentName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1, blank=True, null=True)
    telephone = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    studenttype = models.CharField(db_column='studentType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idno = models.CharField(db_column='idNo', max_length=18, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=50, blank=True, null=True)
    schoolyear = models.DateField(db_column='schoolYear', blank=True, null=True)  # Field name made lowercase.
    avatarurl = models.CharField(db_column='avatarUrl', max_length=4000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student_1'
