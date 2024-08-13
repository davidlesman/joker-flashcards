from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from dotenv import load_dotenv
import google.generativeai as genai
import json
import os

from ai_flashcard import settings
from web.models import Card


with open(settings.BASE_DIR / "system_prompt.txt") as f:
    system_prompt = f.read()

load_dotenv(settings.BASE_DIR / ".env")
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=system_prompt,
    generation_config={"response_mime_type": "application/json"},
)

chat = model.start_chat(history=[])


class IndexPage(View):
    def get(self, request):
        return render(request, "web/index.html")


class CardsPage(View):
    def get(self, request):
        object_list = Card.objects.values("group").distinct()
        print(object_list)
        return render(
            request,
            "web/card_list.html",
            {
                "object_list": object_list,
            },
        )

    def post(self, request):
        print("LOLLLL")
        data = json.loads(request.body)
        object_list = Card.objects.filter(group=data.get("group")).all()
        object_list = {c.pk: c.serialize() for c in object_list}
        return JsonResponse(object_list, status=200)


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
            print(card)
            print(data)
            Card(
                group=user_prompt,
                front=card["front"],
                back=card["back"],
            ).save()

        return HttpResponse(status=201)
