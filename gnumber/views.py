from django.shortcuts import render
from django.views.generic import TemplateView, View
from . import game, rules


class Index(TemplateView):
    template_name = "nav_base.html"
