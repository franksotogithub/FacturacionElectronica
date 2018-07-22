from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic import FormView, View, ListView, UpdateView
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from core.decorators import logged
from django.utils.decorators import method_decorator
from core.mixins import FormAjaxMixin
from .forms import LoginForm
from .models import Usuario
from django.contrib import messages

# Create your views here

class LoginView( FormView):
    form_class = LoginForm
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('webclient:facturas')

    @method_decorator(logged)
    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, *args, **kwargs)

    #def get_context_data(self, **kwargs):
    #    context = super(LoginView, self).get_context_data(**kwargs)
    #    context['nexto'] = '<input type="hidden" name="nexto" value="{}">'.format(self.request.GET.get('nexto'))
    #    print('next to--->',self.request.GET.get('nexto'))
    #    return context


    def form_valid(self, form):
        usuario = form.data.get('usuario')
        password = form.data.get('password')
        nexto = self.request.POST.get('nexto')
        if not (nexto is None):
            self.success_url = nexto
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(reverse('facturacion:facturas'))
        else:
            messages.error(self.request, 'El usuario o password no es correcto!!')
            return super().form_invalid(form)


class CerrarSesionView(View):
    @method_decorator(logged)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('usuarios:login'))