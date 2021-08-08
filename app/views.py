

from rest_framework.response import Response
from rest_framework.views import APIView
from studinfo.rawsql import Sqlca



class UserView(APIView):
    def get(self, request ):
        try:
            results=request.GET.get('results')
            page=request.GET.get('page')
            product=int(results)*(int(page)-1)
            gender = request.GET.get('gender')
            studentType = request.GET.get('studentType')
            searchTerm=request.GET.get('searchTerm')
            print(searchTerm)
            if searchTerm!='null' and searchTerm:
                if searchTerm.isdigit():
                    searchSen='and "studentId" ~ '+'\''+str(searchTerm)+'\''
                    nosearchSen=' where "studentId" ~ '+'\''+str(searchTerm)+'\''
                else:
                    searchSen=' and "studentName" ~ '+'\''+str(searchTerm)+'\''
                    nosearchSen = ' where "studentName" ~ ' + '\'' + str(searchTerm) + '\''
            else:
                searchSen = ''
                nosearchSen =''
            print(searchSen)
            sort=request.GET.get('sortField')
            print(sort)
            sortnow='\"'+sort+'\"'
            print(sortnow)
            order=request.GET.get('sortOrder')
            if order=='ascend':
                order='asc'
                orderTerm=' order by '+sortnow+' '+order
            elif order=='descend':
                order='desc'
                orderTerm = ' order by ' + sortnow + ' ' + order
            else:
                orderTerm=''
            if studentType !='null' and studentType :
                if gender!='null' and gender:
                    sql='select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s and gender=%s '+searchSen+orderTerm+' limit %s offset %s'
                    print(sql)
                    data = Sqlca.execute(sql, [studentType, gender,results,product])
                    sql='select count(gender) from student  where "studentType"= %s and gender=%s '+searchSen
                    count=Sqlca.execute(sql,[studentType, gender])[0]['count']
                else:
                    sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s '+searchSen+orderTerm+' limit %s offset %s '
                    print(sql)
                    data = Sqlca.execute(sql, [studentType,results,product])
                    sql = 'select count(gender) from student  where "studentType"= %s '+searchSen
                    count = Sqlca.execute(sql, [studentType])[0]['count']
            else:
                if gender!='null' and gender:
                    print('hh')
                    sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where gender= %s '+searchSen+orderTerm+' limit %s offset %s'
                    print(sql)
                    data = Sqlca.execute(sql, [gender,results,product])
                    sql = 'select count(gender) from student  where  gender=%s '+searchSen
                    count = Sqlca.execute(sql, [ gender])[0]['count']
                else:
                    sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo"  from student '+nosearchSen+orderTerm+' limit %s offset %s'
                    print(sql)
                    data = Sqlca.execute(sql, [results,product])
                    print((data))
                    sql = 'select count(gender) from student'+nosearchSen
                    count = Sqlca.execute(sql, [])[0]['count']
            rtn={'code':1000,'message':'获取成功','data':data,'count':count}
        except Exception as e:
            rtn = {'code': 1001, 'message': '获取失败'+str(e), 'data': {}}

        return Response(rtn)
    def post(self,request):
        data=request.data
        password=data['idNo'][12:18]
        print(password)
        sql='INSERT INTO student ("studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo",password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            r=Sqlca.execute(sql,[data['studentId'],data['studentName'],data['gender'],data['schoolYear'],data['telephone'],data['email'],data['studentType'],data['idNo'],password])
            rtn = {'code': 1000, 'message': '新增成功', 'data': data,}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '新增失败，失败的详细原因: ' + str(errorDetail), 'data': {}}
        return Response(rtn)

    def put(self, request):
        try:
            data = request.data

            sql = 'update student set "studentName"=%s,gender=%s,"schoolYear"=%s,telephone=%s,email=%s,"studentType"=%s,"idNo"=%s where "studentId"=%s '
            Sqlca.execute(sql,
                          [data['studentName'], data['gender'], data['schoolYear'], data['telephone'], data['email'],
                           data['studentType'], data['idNo'], data['studentId']])

            rtn = {'code': 1000, 'message': '更新成功', 'data': data}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '更新失败，失败的详细原因:'+str(errorDetail), 'data': {}}
        return Response(rtn)

    def delete(self, request):
        try:
            studentId = request.query_params['studentId']
            sql = 'delete from student  where "studentId"=%s '
            Sqlca.execute(sql, [studentId])
            print('yep')
            rtn = {'code': 1000, 'message': '删除成功', 'data': {}}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '删除失败，失败的原因：'+str(errorDetail), 'data': {}}
        return Response(rtn)
class validate(APIView):
    def get(self,request):
        try:
            stuId=request.query_params['studentId']
            print(stuId)
            sql='select count(gender) from student where "studentId"=%s'
            count = Sqlca.execute(sql, [stuId])[0]['count']
            print(count)

            rtn={'code':1000,'message':'获取成功','count':count}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '获取验证失败，失败的原因：' + str(errorDetail)}
        return Response(rtn)
# Create your views here.
