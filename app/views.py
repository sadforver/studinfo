from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student
from django.db.models import Q

class UserView(APIView):
    def get(self,request):
        try:
            pageSize=int(request.GET.get('results'))
            pageIndex=int(request.GET.get('page'))
            Gender = request.GET.get('gender')
            StudentType = request.GET.get('studentType')
            searchTerm=request.GET.get('searchTerm')
            sort = request.GET.get('sortField')
            order=request.GET.get('sortOrder')
            if order=='descend':
                sort='-'+sort
            print(sort)
            if Gender and StudentType:
                q = Q(gender=Gender) & Q(studentType=StudentType)
            elif Gender or StudentType:
                q= Q(gender=Gender) | Q(studentType=StudentType)
            else:
                q=Q()
            print(q)
            if searchTerm!='null' and searchTerm!=None:
                s=Q(studentId__contains=searchTerm)|Q(studentName__contains=searchTerm)
            else:
                s=Q()
            if order!='null'and order!=None:
                studentList=Student.objects.filter(q,s).order_by(sort).values('studentId','studentName','gender','schoolYear','telephone','email','studentType','idNo','avatarUrl')
            else:
                studentList = Student.objects.filter(q,s).order_by().values('studentId', 'studentName', 'gender','schoolYear', 'telephone', 'email','studentType', 'idNo', 'avatarUrl')
            print(studentList)
            total= len(studentList)
            paginator=Paginator(studentList,pageSize)
            page=paginator.get_page(pageIndex).object_list
            print(page)
            things=list(page)
            print(things)
            rtn={'code':1000,'message':'获取成功','data':things,'count':total}
        except Exception as e:
            rtn = {'code': 1001, 'message': '获取失败'+str(e), 'data': {}}
        return Response(rtn)
    def post(self, request):
        data = request.data
        data['password'] = data['idNo'][12:18]
        data['schoolYear']=data['schoolYear'][0:10]
        try:
            Student.objects.create(**data)
            rtn = {'code': 1000, 'message': '新增成功', 'data': data, }
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '新增失败，失败的详细原因: ' + str(errorDetail), 'data': {}}
        return Response(rtn)
    def put(self, request):
        try:
            data = request.data
            id=data['studentId']
            data['schoolYear'] = data['schoolYear'][0:10]
            Student.objects.filter(studentId=id).update(**data)
            rtn = {'code': 1000, 'message': '更新成功', 'data': data}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '更新失败，失败的详细原因:'+str(errorDetail), 'data': {}}
        return Response(rtn)
    def delete(self, request):
        try:
            id = request.query_params['studentId']
            student = Student.objects.filter(studentId=id)
            student.delete()
            rtn = {'code': 1000, 'message': '删除成功', 'data': {}}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '删除失败，失败的原因：'+str(errorDetail), 'data': {}}
        return Response(rtn)

class validate(APIView):
    def get(self,request):
        try:
            id=request.query_params['studentId']
            count=Student.objects.filter(studentId=id).count()
            rtn={'code':1000,'message':'获取成功','count':count}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '获取验证失败，失败的原因：' + str(errorDetail)}
        return Response(rtn)

class photo(APIView):
    def post(self,request):
        try:
            id=request.data['studentId']
            file=request.FILES['avatar']
            file_name=default_storage.save(file.name,file)
            avatar='http://127.0.0.1:8000/media/'+file_name
            Student.objects.filter(studentId=id).update(avatarUrl=avatar)
            rtn = {'code': 1000, 'message': '上传成功', 'data': avatar}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '上传失败，失败的原因：' + str(errorDetail)}
        return Response(rtn)

# Create your views here.