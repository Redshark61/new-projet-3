from django.views import View
from django.shortcuts import render, redirect


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