
import requests
import os
import urllib.parse
from dotenv import load_dotenv
from django.http import JsonResponse

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")

def analyze_review_sentiments(text):
    encoded_text = urllib.parse.quote(text)
    request_url = sentiment_analyzer_url + "analyze/" + encoded_text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
def get_dealer_reviews(request, dealer_id):
    try:
        # Chama a API do backend (Express) para buscar as reviews
        reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")

        # Adiciona sentimento a cada review
        enriched_reviews = []
        if reviews and isinstance(reviews, list):
            for r in reviews:
                sentiment = analyze_review_sentiments(r.get("review", ""))
                enriched_reviews.append({
                    **r,
                    "sentiment": sentiment.get("label", "neutral")
                })

        return JsonResponse({
            "status": 200,
            "reviews": enriched_reviews
        })

    except Exception as e:
        print(f"Erro em get_dealer_reviews: {e}")
        return JsonResponse({"status": 500, "message": "Erro ao buscar reviews"})

