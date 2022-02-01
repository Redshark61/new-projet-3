from django.contrib.auth import authenticate, login as loginUser
from django.shortcuts import redirect, render
from login_signup.models import Job, Doctor, RPPS, CustomUser
from login_signup.forms import *
# Create your views here.


def index(request):
    response = render(request, 'login_signup/index.html')
    response.set_cookie('medical', False)
    if request.method == 'POST':
        person, direction = request.POST.get('button').split("&")
        print(person, direction)

        if person == 'personal':
            response = redirect('login') if direction == 'login' else redirect('login_signup:signup', 1)
            response.set_cookie('medical', False)
            return response

        elif person == 'medical':
            response = redirect('login') if direction == 'login' else redirect(
                'login_signup:signup', 1)
            response.set_cookie('medical', True)
            return response
    return response


def signup(request, number):
    className = eval(f"Connection{number}")
    nextNumber = number + 1
    previousNumber = number - 1
    isMedical = request.COOKIES['medical']
    stepProgress = '12' if isMedical == 'True' else '123456'
    jobs = Job.objects.all() if number == 1 else None
    context = {
        'next_id': nextNumber,
        'current_id': str(number),
        'prev_id': previousNumber,
        'is_medical': True if isMedical == 'True' else False,
        'step_progress': stepProgress,
        'is_valid': True,
        'jobs': jobs,
    }

    if request.method == 'POST':
        form = className.__call__(request.POST)
        context['form'] = form
        if form.is_valid():
            if number == 1:
                user = CustomUser.objects.create_user(
                    username=request.POST['code_id'],
                    email=form.cleaned_data['mail'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'])
                user.save()
                if isMedical == 'True':
                    job = Job.objects.get(name=request.POST['job'])
                    rpps = RPPS.objects.get(rpps=request.POST['code_id'])
                    doctor = Doctor(user=user,
                                    rpps=rpps,
                                    job=job)
                    doctor.save()
                loginUser(request, user)
                return redirect('login_signup:signup', nextNumber)
            if number == 2:
                request.user.birth_date = form.cleaned_data['birth_date']
                request.user.gender = form.cleaned_data['gender']
                request.user.save()
                if isMedical == 'True':
                    return redirect('home:home')
                return redirect('login_signup:signup', nextNumber)
            if number == 3:
                print(request.POST)
                location = form.save(commit=False)
                location.postal_code = request.POST['postal_code']
                location.save()
                request.user.address = location
                request.user.save()
                return redirect('home:home')
        else:
            print("invalid form")
            context['is_valid'] = False
            return render(request, f'login_signup/signup/{number}.html', context)
    else:
        print("in signup else")
        form = className.__call__()
        context['form'] = form
        return render(request, f'login_signup/signup/{number}.html', context)


def login(request):

    def deleteField(request):
        if request.COOKIES['medical'] == 'True':
            del form.fields['id_code']
            return 'rpps_code'
        else:
            del form.fields['rpps_code']
            return 'id_code'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = deleteField(request)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data[username], password=form.cleaned_data['password'])
            if user is not None:
                loginUser(request, user)
                return redirect('home:home')
            else:
                return render(request, 'login_signup/login.html', {'form': form, 'is_valid': False})
        else:
            form = LoginForm()
            deleteField(request)
            return render(request, 'login_signup/login.html', {'is_valid': False, 'form': form})
    else:
        form = LoginForm()
        deleteField(request)

        return render(request, 'login_signup/login.html', {'form': form, 'is_valid': True})
