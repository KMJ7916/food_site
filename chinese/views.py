from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Food
from .models import Category
from django.core.files.storage import FileSystemStorage
# Create your views here.

# def upload(request):
#     fs = FileSystemStorage()
#     uploaded_file = request.FILES['file']
#     name = fs.save(uploaded_file.name, uploaded_file) #파일 저장
#     url = fs.url(name) # 파일 경로를 받아서 DB에 저장
#     return HttpResponse("{}에 저장이 잘 되었습니다.".format(url))
    
    
    
    
def add_food(request):
    if request.method=='GET':
        return render(request=request, template_name='chinese/add_food.html')
    elif request.method =='POST':
        # Category 인스턴스 가져오는 영역
        category = Category.objects.get(name=request.POST['category'])

        # Food 내용을 구성 영역
        food_name = request.POST['lion_name']
        food_price = request.POST['price']
        food_description = request.POST['description']
        
        # 이미지 저장 및 url 설정 내용
        fs=FileSystemStorage()
        uploaded_file = request.FILES['file']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        Food.objects.create(category= category,name=food_name, price =food_price , description=food_description,image_url=url)        
        return redirect('index')  
    
    
def food_delete(request, pk):
    object = Food.objects.get(pk=pk)
    object.delete()
    return redirect('index') 

def food_detail(request, pk):
    object = Food.objects.get(pk=pk)
    context = {
        'object':object
    }
    return render(request, 'chinese/food_detail.html', context)