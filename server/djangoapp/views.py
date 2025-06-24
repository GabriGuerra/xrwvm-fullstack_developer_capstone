from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarMake, CarModel
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"error": "Invalid credentials"})
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return JsonResponse({"error": "Invalid request"})
    return JsonResponse({"error": "POST method required"}, status=400)


@csrf_exempt
def logout_user(request):
    if request.method == "GET":
        logout(request)
        return JsonResponse({"userName": ""})
    return JsonResponse({"error": "GET method required"}, status=400)


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

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Already Registered"})

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.save()
            login(request, user)
            return JsonResponse({"userName": username, "status": "Registered"})
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return JsonResponse({"error": "Invalid request"})
    return JsonResponse({"error": "POST method required"}, status=400)


def get_cars(request):
    if CarMake.objects.count() == 0:
        from .populate import initiate

        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})


def get_dealerships_by_state(request, state):
    dealerships = get_request(f"/fetchDealers/{state}")
    print("Resultado vindo do Express:", dealerships)
    return JsonResponse(dealerships, safe=False)


def get_dealerships(request):
    dealerships = get_request("/fetchDealers")
    return JsonResponse({"dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    try:
        dealership = get_request(f"/fetchDealer/{dealer_id}")
        if dealership:
            return JsonResponse({"status": 200, "dealer": [dealership]})
        else:
            return JsonResponse({"status": 404, "message": "Dealer not found"})
    except Exception as e:
        logger.error(f"Erro em get_dealer_details: {e}")
        return JsonResponse({"status": 500, "message": "Erro ao buscar dealer"})


def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    try:
        reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
        if not reviews or not isinstance(reviews, list):
            return JsonResponse({"status": 500, "message": "Falha ao buscar reviews"})

        for review_detail in reviews:
            text = review_detail.get("review", "")
            sentiment_response = analyze_review_sentiments(text)
            review_detail["sentiment"] = sentiment_response.get("sentiment", "neutral")

        return JsonResponse({"status": 200, "reviews": reviews})
    except Exception as e:
        logger.error(f"Erro em get_dealer_reviews: {e}")
        return JsonResponse({"status": 500, "message": "Erro ao buscar reviews"})


@csrf_exempt
def add_review(request):
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    try:
        data = json.loads(request.body)
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as e:
        logger.error(f"Erro ao postar review: {e}")
        return JsonResponse({"status": 401, "message": "Error in posting review"})
