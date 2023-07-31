from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from padanukkama.models import Pada, Padanukkama

class PadaDetailsView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/pada_details.html'

    def get(self, request, padanukkama_id, pada):
        # Initialize the context dictionary
        context = {}

        padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)
        pada_obj = get_object_or_404(Pada, padanukkama=padanukkama, pada=pada)
        context['pada'] = pada_obj

        return render(request, self.template_name, context)