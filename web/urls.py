from django.urls import path

from web.views import CardsPage, CreateCard, IndexPage, SaveCards


urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("cards/", CardsPage.as_view(), name="cards"),
    # API
    path("create/", CreateCard.as_view(), name="create"),
    path("save/", SaveCards.as_view(), name="save"),
]
