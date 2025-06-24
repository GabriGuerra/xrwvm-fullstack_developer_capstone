import requests
import os
import json
from dotenv import load_dotenv
from django.http import JsonResponse

load_dotenv()

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", default="http://localhost:5050/"
)
print("URL usada para análise:", sentiment_analyzer_url)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None


def analyze_review_sentiments(text):
    import urllib.parse

    encoded_text = urllib.parse.quote(text)
    request_url = sentiment_analyzer_url + "analyze/" + encoded_text
    print(f"🔍 Testando URL: {request_url}")

    try:
        response = requests.get(request_url)
        print(" Resposta recebida:", response.text)
        return response.json()
    except Exception as err:
        print(" Erro na requisição:", err)
        return {"label": "neutral"}


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Post review error: {e}")
        return {"status": 500, "message": "Erro ao enviar review"}


def add_review(request):
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            print(f"Erro ao postar review: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    try:
        reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
        print("📥 Reviews recebidas:", reviews)
        print("✅ Tipo de dado:", type(reviews))

        if not reviews or not isinstance(reviews, list):
            print("⚠️ Reviews inválidas ou vazias")
            return JsonResponse({"status": 500, "message": "Falha ao buscar reviews"})

        enriched_reviews = []
        for r in reviews:
            print("🎯 Analisando review:", r.get("review", ""))
            sentiment = analyze_review_sentiments(r.get("review", ""))
            enriched_reviews.append(
                {**r, "sentiment": sentiment.get("label", "neutral")}
            )

        return JsonResponse({"status": 200, "reviews": enriched_reviews})

    except Exception as e:
        print(f"❌ Erro em get_dealer_reviews: {e}")
        return JsonResponse({"status": 500, "message": "Erro ao buscar reviews"})

    except Exception as e:
        print(f"Erro em get_dealer_reviews: {e}")
        return JsonResponse({"status": 500, "message": "Erro ao buscar reviews"})
