from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = "djangoapp"

urlpatterns = [
    # path for registration
    path("register", views.register_user, name="register"),
    # path for login
    path("login", views.login_user, name="login"),
    # path for logout
    path("logout", views.logout_user, name="logout"),
    # path for getting the list of cars (CarMake and CarModel)
    path("get_cars", views.get_cars, name="getcars"),
    path(route="get_dealers/", view=views.get_dealerships, name="get_dealers"),
    path(
        route="get_dealers/<str:state>/",
        view=views.get_dealerships_by_state,
        name="get_dealers_by_state",
    ),
    path(
        route="dealer/<int:dealer_id>",
        view=views.get_dealer_details,
        name="dealer_details",
    ),
    path(
        route="reviews/dealer/<int:dealer_id>",
        view=views.get_dealer_reviews,
        name="dealer_reviews",
    ),
    path(route="add_review", view=views.add_review, name="add_review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
