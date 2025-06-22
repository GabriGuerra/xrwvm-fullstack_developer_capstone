from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, analyze_review_sentiments, post_review
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Login view para autenticação de usuário
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = {"userName": username, "status": "Authenticated"}
            else:
                response = {"error": "Invalid credentials"}
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            response = {"error": "Invalid request"}
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "POST method required"}, status=400)

# Logout view aceita GET para logout conforme a necessidade
@csrf_exempt
def logout_user(request):
    if request.method == 'GET':
        logout(request)
        data = {"userName": ""}
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "GET method required"}, status=400)

# Registration view para criação de novo usuário e login automático
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            email = data.get("email")

            # Verifica se já existe usuário com mesmo username
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Already Registered"})

            # Cria usuário
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.save()

            # Loga o usuário automaticamente após registro
            login(request, user)

            return JsonResponse({"userName": username, "status": "Registered"})
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return JsonResponse({"error": "Invalid request"})
    else:
        return JsonResponse({"error": "POST method required"}, status=400)

# Import necessário para get_cars
from .models import CarMake, CarModel

def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        from .populate import initiate
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})
def get_dealerships_by_state(request, state):
    from .restapis import get_request
    endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    print("Resultado vindo do Express:", dealerships)
    return JsonResponse(dealerships, safe=False)
def get_dealerships(request):
    from .restapis import get_request
    endpoint = "/fetchDealers"
    dealerships = get_request(endpoint)
    return JsonResponse({"dealers": dealerships})

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
#def get_dealerships(request, state="All"):
#    if(state == "All"):
#        endpoint = "/fetchDealers"
#    else:
#        endpoint = "/fetchDealers/"+state
#    dealerships = get_request(endpoint)
#    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def add_review(request):
    if request.user.is_anonymous == False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})