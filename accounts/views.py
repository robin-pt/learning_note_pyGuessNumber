""" extend generic forms """
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views import View


class Signin(LoginView):
    """ extend generic login view. """
    template_name = 'registration/login.html'

    def redirectTo(self):
        """ redirect to index. """
        return HttpResponseRedirect(reverse('gnumber:index'))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.redirectTo()
        return super(Signin, self).dispatch(request, *args, **kwargs)


class SignUp(View):
    """ simple  """
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', locals())

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:user_login'))
