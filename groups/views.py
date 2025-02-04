from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.forms import Form
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = "groups/index.html"

    def get(self, request: HttpRequest):
        context = {}
        if request.method == "GET":
            setting = request.GET.get("setting", None)
            if setting == "true":
                context["setting"] = True

        return render(request, self.template_name, context=context)
