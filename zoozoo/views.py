from django.views.generic import ListView, DetailView, TemplateView

class Index(TemplateView):
    template_name = 'index.html'

class Research(TemplateView):
    template_name = 'research.html'