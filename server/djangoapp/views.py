from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
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

# (Outras views podem ser adicionadas abaixo)
