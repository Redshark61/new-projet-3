from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from login_signup.models import Treatment, Appointment, UserDisease
from .forms import UserForm, PasswordChangingForm


@method_decorator(login_required(login_url='index'), name="get")
class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        appointment = Appointment.objects.filter(user=request.user)
        print(appointment)
        context = {
            'user': request.user,
            'appointments': appointment,
        }

        return render(request, self.template_name, context)


class DiseasesView(ListView):
    model = UserDisease
    template_name = 'home/diseases.html'
    # context_object_name = 'disease_list'

    def get_queryset(self):
        queryset = super(DiseasesView, self).get_queryset()
        userDiseases = queryset.filter(user=self.request.user)
        # # print(userDiseases.get(username=self.request.user))
        print(userDiseases)
        return userDiseases


class TreatmentsView(ListView):
    model = Treatment
    template_name = 'home/treatments.html'

    def get_queryset(self):
        queryset = super(TreatmentsView, self).get_queryset()
        userTreatments = queryset.filter(User_treatment=self.request.user)
        print(userTreatments)
        return userTreatments


class SettingsView(View):
    template_name = 'home/settings.html'

    def get(self, request):
        form = UserForm(instance=request.user)

        context = {
            'user': request.user,
            'form': form,
            'is_medical': request.COOKIES.get('is_medical'),
            'is_valid': True
        }

        return render(request, self.template_name, context)

    def post(self, request):
        # check whether the button clicked had the value delete or not
        if request.POST.get('button') == 'delete':
            return redirect('home:delete')
        else:
            form = UserForm(request.POST, instance=request.user)
            print(form.errors)
            print(form.cleaned_data)
            print(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home:settings')
            context = {
                'form': form,
                'is_valid': False
            }
            return render(request, self.template_name, context)


class DeleteView(View):
    template_name = 'home/delete.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.POST.get('button') == 'delete':
            request.user.delete()
            return redirect('index')
        else:
            return redirect('home:settings')


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'home/change_password.html'
    success_url = reverse_lazy('home:password_success')


def passwordSuccess(request):
    return render(request, 'home/password_success.html')


class AppointmentsView(ListView):
    model = Appointment
    template_name = 'home/appointments.html'

    def get_queryset(self):
        queryset = super(AppointmentsView, self).get_queryset()
        print(queryset)
        userAppointments = queryset.filter(user=self.request.user)
        print(userAppointments)
        return userAppointments
