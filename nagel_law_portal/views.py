import os
import json
import requests
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import forms, category, upload_file
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from nagel_law_portal.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from nagel_law_portal.services.s3_service import upload_to_s3
from nagel_law_portal.constants.prompts import (
    LAW_FIRM_SYSTEM_PROMPT
)


INCEPTION_API_KEY = getattr(settings, "INCEPTION_API_KEY", None)
INCEPTION_URL = "https://api.inceptionlabs.ai/v1/chat/completions"


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@csrf_exempt
def chat_view(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    # Parse request JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON body")

    message = data.get("message")
    context = data.get("context", "")

    if not message:
        return HttpResponseBadRequest("`message` field required")

    print("API CALL RECEIVED")
    print("CHAT CALL message send:", message)
    print("CHAT CALL context send:", context)

    try:
        # Send request to OpenAI
        headers = {
            "Authorization": f"Bearer {INCEPTION_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "mercury",
            "messages": [
                {"role": "system", "content": "You are an assistant helping the user understand the current web page content."},
                {"role": "user", "content": f"Page context: {context or 'unknown'}"},
                {"role": "user", "content": message},
            ],
        }

        response = requests.post(INCEPTION_URL, headers=headers, json=payload)
        data = response.json()
        print("API CALL COMPLETED", data)

        if response.status_code != 200:
            error_message = data.get("error", {}).get("message", "Unknown error")
            print("OpenAI API error:", data)
            return JsonResponse({"reply": f"OpenAI Error: {error_message}"}, status=500)

        reply = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "Sorry, I couldn't generate a response.")
        )

        return JsonResponse({"reply": reply})

    except Exception as e:
        print("Chat server error:", str(e))
        return JsonResponse({"reply": "Error contacting INCEPTION API."}, status=500)

@csrf_exempt
def general_law_chat_view(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    # Parse request JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON body")

    message = data.get("message")
    if not message:
        return HttpResponseBadRequest("`message` field required")

    try:
        headers = {
            "Authorization": f"Bearer {INCEPTION_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "mercury",
            "messages": [
                {"role": "system", "content": LAW_FIRM_SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
        }

        response = requests.post(INCEPTION_URL, headers=headers, json=payload)
        data = response.json()

        if response.status_code != 200:
            error_message = data.get("error", {}).get("message", "Unknown error")
            print("INCEPTION API error:", data)
            return JsonResponse({"reply": f"API Error: {error_message}"}, status=500)

        reply = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "Sorry, I couldn't generate a response.")
        )

        return JsonResponse({"reply": reply})

    except Exception as e:
        print("Law chat server error:", str(e))
        return JsonResponse({"reply": "Error contacting INCEPTION API."}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_forms(request):
    forms_data = list(forms.objects.values())
    return JsonResponse(forms_data, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_categories(request):
    categories_data = list(category.objects.values())
    return JsonResponse(categories_data, safe=False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_file_api(request):
    details = {k: v[0] for k, v in request.POST.copy().lists()}
    uploaded_file = request.FILES.get("file")
    filename = details.get("filename")
    
    if not uploaded_file:
        return HttpResponseBadRequest("No file uploaded.")
    
    if not filename:
        return HttpResponseBadRequest("Filename is required.")
    
    file_url = upload_to_s3(uploaded_file)
    
    data = {
        "file_name": filename,
        "uploaded_file": file_url,
    }
    
    obj = upload_file.objects.create(**data)

    if obj:
        return JsonResponse({"message": "File uploaded successfully.", "file_id": obj.id})
    else: 
        return JsonResponse({"message": "File upload failed."}, status=500)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_uploaded_files_api(request):
    files_data = list(upload_file.objects.values())
    return JsonResponse(files_data, safe=False)