import logging

from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class IndexPage(TemplateView):
    template_name = 'index.html'
    extra_context = {"title": "Главная страница"}
