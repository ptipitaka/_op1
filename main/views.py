from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_name"] = _("OPENPĀḶI")
        return context
    
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/change_password.html', {
        'form': form
    })