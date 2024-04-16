from django.shortcuts import render
from chinese.models import Category, Food
from .models import Cart
# Create your views here.
def customer_index(request):
    # category, food 보내줘야 돼 -> category만 가져와도 food 가져와짐(foreignkey)
    category = Category.objects.all()
    context={
        'category' : category
    }
    return render(request,'customer/index.html',context)

def food_detail(request,pk):
    # object 필요함
    food = Food.objects.get(pk=pk)
    context={
        'object': food
    }
    return render(request, 'customer/customer_detail.html',context)

def add_cart(request):
    # Cart food_id에 대응되는 데이터의 수량을 add 하다(하나 올려라)
    food_id = request.GET['food_id']
    food = Food.objects.get(pk=food_id)
    # 이전에 해당 음식에 대한 장바구니 정보가 있으면 get
    # 없으면 새로 생성해서 적용
    try:
        cart = Cart.objects.get(food=food)
    except:
        cart = Cart.objects.create(food=food)
    finally:
        pass
    cart.amount+=1
    cart.save()
    context = {
        'object':food
    }
    return render(request, 'customer/customer_detail.html',context )

def remove_cart(request):
    food_id= request.GET['food_id']
    food = Food.objects.get(pk=food_id)
    cart = Cart.objects.get_or_create(food=food)
    # cart, created = Cart.objects.get_or_create(food=food)    
    cart, _ = Cart.objects.get_or_create(food=food)   
    cart.amount-=1
    cart.save()
    context = {
        'object':food
    }
    return render(request, 'customer/customer_detail.html',context )

from django.http import JsonResponse
def modify_cart(request):
    # 어떤 음식(food_id)에 amount를 amountChange만큼 변경하고 -> 개발하기
    food_id= request.POST['foodId']
    food = Food.objects.get(pk=food_id)
    cart, _ = Cart.objects.get_or_create(food=food)
    cart.amount+=int(request.POST['amountChange'])
    if cart.amount>0:
        cart.save()
    # 변경된 최종 결과를 반환(JSON 형식)
    context={
        'newQuantity': cart.amount,
        'message':'수량이 성공적으로 업데이트 되었습니다.',
        'success':True
    }
    return JsonResponse(context)
    # request.POST : <QueryDict: {'foodId': ['4'], 'amountChange': ['1']}> 기반으로 위 내용 ->