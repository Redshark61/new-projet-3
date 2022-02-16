from django.views.generic.list import ListView
from login_signup.models.treatment import Treatment
from login_signup.models.prescription import Prescription


class TreatmentsView(ListView):
    """
    Display the treatments for the current user
    """

    model = Treatment
    template_name = 'home/treatments.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        userTreatments = queryset.filter(User_treatment=self.request.user)
        print(userTreatments)
        return userTreatments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prescriptions'] = Prescription.objects.filter(user=self.request.user)
        return context
