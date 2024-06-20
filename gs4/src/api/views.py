from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Student
from .serializer import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
# Create your views here.\
@method_decorator(csrf_exempt,name='dispatch')
class StudentAPI(View):
    def get(self,request, *args,**kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id',None)
        if id is not None:
            stu = Student.objects.get(id=id) 
            serailizer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serailizer.data)
            return HttpResponse(json_data,content_type='application/json')
        stu = Student.objects.all()
        serailizer = StudentSerializer(stu, many = True)
        json_data = JSONRenderer().render(serailizer.data)
        return HttpResponse(json_data,content_type='application/json')

    def post(self, request,*args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serailizer = StudentSerializer(data=pythondata)
        if serailizer.is_valid():
            serailizer.save()
            res = {'msg':'data saved'} 
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data = JSONRenderer().render(serailizer.errors)
        return HttpResponse(json_data,content_type='application/json')
    
    
    def put(self,request,*args, **kwargs ):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        serailizer = StudentSerializer(stu,data=pythondata, partial=True)
        if serailizer.is_valid():
            serailizer.save()
            res = {'msg':'data updated'} 
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data = JSONRenderer().render(serailizer.errors)
        return HttpResponse(json_data,content_type='application/json')
    

    def delete(self,request,*args, **kwargs ):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        stu.delete()
        res = {'msg' :'data deleted'}
        # json_data = JSONRenderer().render(res)
        # return HttpResponse(json_data,content_type='application/json')
        return JsonResponse(res, safe=False)