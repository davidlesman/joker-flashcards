from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
import google.generativeai as genai
import json
import stripe

from ai_flashcard import settings
from web.models import Card, Premium

# API
genai.configure(api_key=settings.GEMINI)
stripe.api_key = settings.PRIVATE_STRIPE


with open(settings.BASE_DIR / "system_prompt.txt") as f:
    system_prompt = f.read()

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=system_prompt,
    generation_config={"response_mime_type": "application/json"},
)

chat = model.start_chat(history=[])


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class IndexPage(View):
    def get(self, request):
        if Premium.objects.get(ip_address=get_client_ip(request)):
            premium = True
        else:
            premium = False
        return render(
            request,
            "web/index.html",
            {
                "premium": premium,
            },
        )


class CardsPage(View):
    def get(self, request):
        object_list = Card.objects.values("group").distinct()
        return render(
            request,
            "web/card_list.html",
            {
                "object_list": object_list,
            },
        )

    def post(self, request):
        data = json.loads(request.body)
        object_list = Card.objects.filter(group=data.get("group")).all()
        object_list = {c.pk: c.serialize() for c in object_list}
        return JsonResponse(object_list, status=200)


class PremiumPage(TemplateView):
    template_name = "web/premium.html"


class SuccessView(View):
    def get(self, request):
        # Add premium role to user
        Premium(ip_address=get_client_ip(request)).save()
        return render(request, "web/success.html")


class CancelledView(TemplateView):
    template_name = "web/cancelled.html"


class StripeConfig(View):
    @csrf_exempt
    def get(self, request):
        stripe_config = {"publicKey": settings.PUBLIC_STRIPE}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.PRIVATE_STRIPE
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "product_data": {
                                "name": "premium",
                                "description": "Lifetime premium for Joker.",
                            },
                            "currency": "eur",
                            "unit_amount": "1500",
                        },
                        "quantity": 1,
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class CreateCard(View):
    def post(self, request):
        data = json.loads(request.body)
        response = chat.send_message(data.get("userInput"))

        return JsonResponse(json.loads(response.text), status=200)


class SaveCards(View):
    def post(self, request):
        data = json.loads(request.body)
        user_prompt = data.get("userPrompt")
        for card in data.get("cards")["flashcards"]:
            Card(
                group=user_prompt.title(),
                front=card["front"],
                back=card["back"],
            ).save()

        return HttpResponse(status=201)
