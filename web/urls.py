from django.urls import path

from web.views import (
    CancelledView,
    CardsPage,
    CreateCard,
    IndexPage,
    PremiumPage,
    SaveCards,
    StripeConfig,
    SuccessView,
    create_checkout_session,
)


urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("cards/", CardsPage.as_view(), name="cards"),
    path("premium/", PremiumPage.as_view(), name="premium"),
    path("success/", SuccessView.as_view()),  # new
    path("cancelled/", CancelledView.as_view()),
    # API
    path("config/", StripeConfig.as_view(), name="config"),
    path("create/", CreateCard.as_view(), name="create"),
    path("create-checkout-session/", create_checkout_session),
    path("save/", SaveCards.as_view(), name="save"),
]
