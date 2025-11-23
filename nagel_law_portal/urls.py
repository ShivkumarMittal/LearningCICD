from django.urls import path
from .views import chat_view, get_uploaded_files_api, upload_file_api, get_forms, get_categories, CustomTokenObtainPairView, get_uploaded_files_api, general_law_chat_view


urlpatterns = [
    path("chat/", chat_view, name="chat"),
    path("general_law_chat/", general_law_chat_view, name="general_law_chat"),
    path("forms/", get_forms, name="forms"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("categories/", get_categories, name="categories"),
    path("upload_file/", upload_file_api, name="upload_file"),
    path("files/", get_uploaded_files_api, name="files"),
]
