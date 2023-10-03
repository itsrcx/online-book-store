from django.views import generic
from .forms import NewUserForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound

def catch_all_view(request):
    return HttpResponseNotFound("You know this page doesn't exist. 	&#128521; #404")

class UserRegistraion(generic.CreateView):
    form_class = NewUserForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(1800)  
        return super().form_valid(form)