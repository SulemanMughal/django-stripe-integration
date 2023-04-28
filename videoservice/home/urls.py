from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("details/<slug>/", views.details, name="details"),
    path("become-pro/", views.BecomePro, name="BecomePro"),
    path("create-payment-intent/", views.create_payment),
    path("charge/", views.charge, name="charge"),
]