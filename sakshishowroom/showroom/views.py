from django.shortcuts import render
from . import models
from django.shortcuts import redirect
from django.contrib.auth.models import User
import random
from django.contrib.auth import authenticate, login as userLogin,logout as userLogout
import razorpay
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
# Create your views here.
import random_id


def home(request):
    if request.method == 'GET':
        cart_clear = request.GET.get('cart')
        
        if(cart_clear == 'clear'):request.session['cart'] = {}

        products = models.Product.get_all()
        slider = random.sample(list(products), 5)

        top_deals = random.sample(list(products),4)
        pfu = random.sample(list(products),4)
        
        context = {
            "products": products,
            "slider":slider,
            "top_deals": top_deals,
            "pfu": pfu,
        }
        
        try:cart = request.session['cart']
        except:cart = {}
        finally:
            pid_array = []
            for key,val in cart.items():
                pid_array.append(int(key))
            
            context['cart_items_array'] = pid_array
        return render(request, 'showroom/home.html', context)



def show_product(request):
    pid = int(request.GET['id'])
    product = models.Product.get_by_id(pid)
    return render(request, 'showroom/product_view.html', {"product": product},)

    


def about(request):
    products = models.Product.get_all()

    slider = random.sample(list(products), 5)

    return render(request, 'showroom/about.html', {"slider":slider},)



def LogOut(request):
    userLogout(request)
    return redirect('../../showroom')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            userLogin(request, user)
            return redirect('../../showroom')
        else:
            return render(request, 'showroom/login.html', {"error":"Invalid username or password"})

    else:
        return render(request, 'showroom/login.html')


def register(request):
    if request.method == 'POST':
        userName = request.POST.get('userName')
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword')

        user = User.objects.create_user(
            username=userEmail,
            first_name=userName,
            password= userPassword
        )
        user.save()

        n = authenticate(request,  username = userEmail, password =  userPassword )
        userLogin(request, n)
        
        return redirect('../../showroom')
    else:
        return render(request, 'showroom/register.html')
    


def UserProfile(request):
    products = models.Product.get_all()

    slider = random.sample(list(products), 5)
    
    if request.user.is_authenticated:
        return render(request, 'showroom/profile.html', {"slider": slider, "user":request.user})
    else:
        return redirect('../../showroom/login')
    

@csrf_exempt
def AddToCart(request):
    pid = request.POST.get('item')
    # request.session.__delitem__("cart")
    try:
        cart = request.session['cart']
    except:
        request.session['cart'] = {}
        cart = request.session['cart']
    
    finally:
        # request.session['cart'] = cart
        try:
            cart[pid] += 1

        except KeyError:
            # prev_qtty = cart[pid]
            cart[pid] = 1
        finally:request.session['cart'] = cart
    
    print(cart)
    return JsonResponse({"status": "success"} )


@csrf_exempt
def RemoveFromCart(request):
    pid = request.POST.get('item')

    cart = request.session["cart"]
    
    prev_qtty = cart[pid]
    print(prev_qtty, type(prev_qtty))
    new_qtty = prev_qtty - 1

    if(new_qtty <= 0):
        cart.__delitem__(pid)
    else:
        cart[pid] = new_qtty
    request.session["cart"] = cart

    print(cart)
    return JsonResponse({"status": "success"} )





def CreateRazorPayOrder(amount):
    client = razorpay.Client(auth=("rzp_test_VQbLxtPQlLLxGQ", "pYERoBVS98XnYmwD8SF0LMNm"))
    DATA = {
        "amount": amount,
        "currency": "INR",
        "receipt": random_id.random_id(),
    }
    return client.order.create(data=DATA)
    



def ShowCartItems(request):
    if request.method == 'GET' and request.user.is_authenticated:
        products = models.Product.get_all()
        slider = random.sample(list(products), 5)

        cart = request.session.get('cart')

        print(cart)

        context = {
            "slider": slider,
        }
        if cart != None and cart != '{}':
            total_amount = 0
            products = []
            
            for pid,qtty in cart.items():
                product = models.Product.get_by_id(int(pid))
                products.append((product, qtty))
                total_amount += (product.price * qtty)

            context['products'] = products
            context['total_amount'] = total_amount


        return render(request, 'showroom/show_cart.html',context=context)
    elif request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        total_amount = 0
        products = []
        cart = request.session.get('cart')

        for pid,qtty in cart.items():
            product = models.Product.get_by_id(int(pid))
            total_amount += (product.price * qtty)

        razor_pay_order = CreateRazorPayOrder((total_amount*100))
        order = models.Order.objects.create(
            phone= phone,
            address= address,
            order_id = razor_pay_order['id'],
            order_amount = razor_pay_order['amount'],
            order_user =  User.objects.get(username=request.user.username),
            order_products = json.dumps(cart),
        )
        order.save()

        return JsonResponse({"status": "success","keyid":"rzp_test_VQbLxtPQlLLxGQ","user":request.user.username,"phone":phone,"address":address,"razor_pay_order":razor_pay_order })
    else:
        return redirect('../../showroom/login')


def VerifyPayment(request):
    client = razorpay.Client(auth=(("rzp_test_VQbLxtPQlLLxGQ", "pYERoBVS98XnYmwD8SF0LMNm")))

    razorpay_order_id=  request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_signature =  request.POST.get('razorpay_signature')

    order = models.Order.GetByOrderId(razorpay_order_id)
    order.razorpay_payment_id=razorpay_payment_id
    order.razorpay_signature=razorpay_signature
    try:
        # // payment success
        client.utility.verify_payment_signature({
        'razorpay_order_id':razorpay_order_id,
        'razorpay_payment_id':razorpay_payment_id ,
        'razorpay_signature':razorpay_signature
        })
        order.payment_status="paid"
        order.save()
        return JsonResponse({"status": "success"})
    except Exception as e:
        order.payment_status="failed"
        order.save()
        print(e)
        return JsonResponse({"status":'failed'})

    

def OrdersListing(request):
    products = models.Product.get_all()
    slider = random.sample(list(products), 5)

    orders = models.Order.get_by_user(request.user)

    order = []

    for i in orders:
        temp = []
        pid = json.loads(i.order_products)
        
        for product in pid.keys():
            temp.append(models.Product.get_by_id(int(product)))
        
        order.append( (i, temp) )

    return render(request, 'showroom/orderlisting.html', {"slider": slider, "orders": order})