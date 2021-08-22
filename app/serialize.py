
from rest_framework import serializers
from app.models import Student

class StudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('studentId',
                  'studentName',
                  'gender',
                  'telephone',
                  'email',
                  'studentType',
                  'idNo',
                  # 'password',
                  'schoolYear',
                  'avatarUrl')
