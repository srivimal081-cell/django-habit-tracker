import json
import os
from .models import AuthToken
from .models import Habit
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet, InvalidToken
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

STORAGE_FILE = "storage.json"


def load_data():
    if not os.path.exists("storage.json"):
        with open("storage.json", "w") as f:
            f.write("[]")

    with open("storage.json", "r") as f:
        return json.load(f)


def save_data(data):
    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file, indent=4)


habits = load_data()

@csrf_exempt
def create_habit(request):

    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    token = request.META.get("HTTP_AUTHORIZATION")

    if not token:
        return JsonResponse({"error": "Token required"}, status=401)

    try:
        token_obj = AuthToken.objects.get(token=token)
        user = token_obj.user
    except AuthToken.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)

   
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
         data = request.POST

    habit_name = data.get("habit_name")
    description = data.get("description")
    frequency = data.get("frequency")
    start_date = data.get("start_date")

    if not habit_name or not description or not frequency or not start_date:
        return JsonResponse({"error": "All fields required"}, status=400)

   
    habit = Habit.objects.create(
        user=user,
        habit_name=habit_name,
        description=description,
        frequency=frequency,
        start_date=start_date
    )

    return JsonResponse({
        "message": "Habit created successfully",
        "id": habit.id
    }, status=200)

def get_habits(request):

    token = request.META.get("HTTP_AUTHORIZATION")

    if not token:
        return JsonResponse({"error": "Token required"}, status=401)

    try:
        token_obj = AuthToken.objects.get(token=token)
    except AuthToken.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)

    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)

    user = token_obj.user

    result = [h for h in habits if h.get("user") == user.username]

    return JsonResponse(result, safe=False)

def get_habit(request, id):

    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)

    for habit in habits:
        if habit["id"] == id:
            return JsonResponse(habit)

    return JsonResponse({"error": "Habit not found"}, status=404)

@csrf_exempt
def delete_habit(request, id):

    global habits

    if request.method != "DELETE":
        return JsonResponse({"error": "Only DELETE method allowed"}, status=405)

    for habit in habits:
        if habit["id"] == id:
            habits.remove(habit)

            save_data(habits)   

            return JsonResponse({"message": "Habit deleted"})

    return JsonResponse({"error": "Habit not found"}, status=404)

@csrf_exempt
def update_habit(request, id):

    global habits

    if request.method != "PUT":
        return JsonResponse({"error": "Only PUT method allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    name = data.get("name")
    frequency = data.get("frequency")
    date = data.get("date")

    for habit in habits:
        if habit["id"] == id:

            if name:
                habit["name"] = name
            if frequency:
                habit["frequency"] = frequency
            if date:
                habit["date"] = date

            save_data(habits)

            return JsonResponse(habit)

    return JsonResponse({"error": "Habit not found"}, status=404)



def download_documentation(request):
    file_path = os.path.join(settings.BASE_DIR, "documentation.pdf")
    return FileResponse(open(file_path, "rb"), as_attachment=True)


def home(request):
    return render(request, "index.html")

def habit_count(request):

    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)

    return JsonResponse({"count": len(habits)})

def export_data(request):

    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)

    file = open("storage.json", "rb")

    return FileResponse(file, as_attachment=True, filename="storage.json")

   
def export_encrypted_data(request):

    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)

    from crypto_utils import load_key

    key = load_key()
    f = Fernet(key)

    with open("storage.json", "rb") as file:
        data = file.read()

    encrypted_data = f.encrypt(data)

    with open("storage_encrypted.bin", "wb") as file:
        file.write(encrypted_data)

    return FileResponse(
        open("storage_encrypted.bin", "rb"),
        as_attachment=True,
        filename="storage_encrypted.bin"
    )


@csrf_exempt
def reset_storage(request):

    global habits

    if request.method != "DELETE":
        return JsonResponse({"error": "Only DELETE method allowed"}, status=405)

    habits = []

    with open("storage.json", "w") as file:
        json.dump([], file)

    return JsonResponse({"message": "Storage cleared"})

@csrf_exempt
def login_view(request):

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("username")
    password = data.get("password")

    if not username:
        return JsonResponse({"error": "Username required"}, status=400)

    if not password:
        return JsonResponse({"error": "Password required"}, status=400)

    user = authenticate(request, username=username, password=password)

    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    token_obj, created = AuthToken.objects.get_or_create(user=user)

    return JsonResponse({
        "message": "Login successful",
        "token": token_obj.token
    })


def decrypt_data(request):

    key = request.GET.get("key")

    if not key:
        return JsonResponse({"error": "Key required"}, status=400)

    try:
        f = Fernet(key.encode())

        with open("storage_encrypted.bin", "rb") as file:
            encrypted_data = file.read()

        decrypted = f.decrypt(encrypted_data)

        return JsonResponse({
            "message": "Decryption successful",
            "data": decrypted.decode()
        })

    except (InvalidToken, ValueError):  
        return JsonResponse({
            "error": "Invalid key. Cannot decrypt data."
        }, status=400)
def search_habits(request):

    token = request.META.get("HTTP_AUTHORIZATION")

    if not token:
        return JsonResponse({"error": "Token required"}, status=401)

    try:
        token_obj = AuthToken.objects.get(token=token)
        user = token_obj.user
    except AuthToken.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)

    keyword = request.GET.get("q", "")

    habits = Habit.objects.filter(
        user=user,
        habit_name__icontains=keyword
    )

    data = []
    for habit in habits:
        data.append({
            "id": habit.id,
            "habit_name": habit.habit_name,
            "description": habit.description
        })

    return JsonResponse(data, safe=False)