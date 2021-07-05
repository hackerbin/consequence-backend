from django.urls import path

from truelayer.views import CallbackAPIView, BanksAPIView, CardsAPIView, LinkAccount

app_name = 'truelayer'
urlpatterns = [
    path('login', CallbackAPIView.as_view()),
    path('accounts', BanksAPIView.as_view()),
    path('cards', CardsAPIView.as_view()),
    path('link-account', LinkAccount.as_view()),
    path('account-transactions', CallbackAPIView.as_view()),
    path('card-transactions', CallbackAPIView.as_view()),
]
