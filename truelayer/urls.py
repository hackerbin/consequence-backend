from django.urls import path

from truelayer.views import CallbackAPIView, BanksAPIView, CardsAPIView, LinkAccount, GetAccount, GetLinkedAccounts, \
    GetLinkedTransactions

app_name = 'truelayer'
urlpatterns = [
    path('login', CallbackAPIView.as_view()),
    path('bank-accounts', BanksAPIView.as_view()),
    path('cards', CardsAPIView.as_view()),
    path('link-account', LinkAccount.as_view()),
    path('get-account', GetAccount.as_view()),  # only for debugging purpose not used in frontend
    path('get-linked-accounts', GetLinkedAccounts.as_view()),
    path('get-linked-transactions', GetLinkedTransactions.as_view()),
    path('account-transactions', CallbackAPIView.as_view()),
    path('card-transactions', CallbackAPIView.as_view()),
]
