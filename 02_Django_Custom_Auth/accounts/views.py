from django.contrib import messages
from django.contrib.auth import login, logout, mixins
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View

from accounts.forms import ProfileUpdateForm
from accounts.models import User


# Create your views here.
#D Dashboard
class DashboardView(mixins.LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/dashboard.html')


# Profile
class ProfileView(mixins.LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile.html'
    # image = User.objects.values('profile_pic')
    fields = ('first_name','last_name', 'username','email',
            'phone_number', 'roll', 'age', 'gender', 'profile_pic',
            'bio')
    # success_url = reverse_lazy("accounts:profile")
    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.object.pk})

    # def get_object(self, queryset=None):
    #     obj = User.objects.get(id=self.kwargs['id'])
    #     return obj

    # def get_object(self, queryset = None):
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #     return get_object_or_404(queryset, users_id = self.kwargs['pk'])

# def profile_view(request, pk):
#     if request.method=="POST":
#         form = ProfileUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#     form = ProfileUpdateForm()

#     return render(request,'accounts/profile.html', {'form':form})


# LogIn
class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return render(request, 'accounts/login.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        if username.isnumeric():
            phone = username
        else:
            phone = None

        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username) | Q(phone_number=phone)
            )

        except User.DoesNotExist:
            return None

        # if user and check_password(password, user.password):
        #     return user

        # user = User.objects.get(
        #     Q(username=username) | Q(email=username) | Q(phone_number=username)
        # )

        PWD = check_password(password, user.password)

        if user is not None and PWD is True:
            user = user

        error_message = False

        if user is not None and user.is_active is True:
            login(request, user)
            return user and redirect('accounts:dashboard')
        else:
            error_message = "Invalid username or password"

        return render(request, 'accounts/login.html', {
            "error_message": error_message,})


# Logout
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        if 'next' in request.GET.keys():
            return redirect(request.GET['next'])
        return redirect("home")


# SignUp
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/register.html', {})

    def post(self, request, *args, **kwargs):
        # breakpoint()

        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            role = request.POST['roll']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            password2 = request.POST['confirm_password']

            # breakpoint()
            if password == password2:
                eml = User.objects.filter(email=email).exists()
                phn = User.objects.filter(phone_number=phone).exists()
                if eml and phn:
                    messages.info(request, 'Email & Phone already exist.')
                    return redirect('accounts:register')
                elif eml:
                    messages.info(request, 'Email! already exist.')
                    return redirect('accounts:register')
                elif phn:
                    messages.info(request, 'Phone! already exist.')
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(username=None, first_name=first_name,
                        last_name=last_name, email=email, phone_number=phone,
                        password=password)
                    user.roll = role
                    user.save()
                    return redirect('accounts:login')
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('accounts:register')
        else:
            return render(request, 'accounts/register.html')
