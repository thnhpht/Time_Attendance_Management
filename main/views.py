from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages


User = get_user_model()


@login_required(login_url='sign-in')
def home(request):
    if not request.user.is_authenticated:
        return redirect('/sign-in/')
    return render(request, 'home.html')


def authenticate_user(email=None, password=None):
    try:
        user = User.objects.get(email=email)

        if check_password(password, user.password):
            return user
        return None
    except User.DoesNotExist:
        return None


def sign_in(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate_user(email, password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Đăng nhập thành công')
            return redirect('/home/')
        else:
            messages.warning(request, 'Email hoặc mật khẩu không chính xác')
    return render(request, 'sign-in.html')


def sign_up(request):
    if request.method == "POST":
        name = request.POST.get('name')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        image = request.FILES.get('image')

        try:
            User.objects.get(email=email)
            messages.warning(request, 'Email đã tồn tại')
        except User.DoesNotExist:
            if password1 == password2:
                user = User.objects.create_user(email=email, name=name, tel=tel, image=image, password=password1)
                user.save()
                messages.success(request, 'Tạo tài khoản thành công')
            else:
                messages.warning(request, 'Mật khẩu và mật khẩu xác nhận khác nhau')
    return render(request, 'sign-up.html')


def sign_out(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công')
    return redirect('/sign-in/')


def user(request):
    id = request.user.id
    print(id)
    user = User.objects.get(id=id)
    return render(request, 'user.html', {
        'user': user,
    })


def staff(request):
    user = User.objects.all()
    return render(request, 'staff.html', {
        'users': user,
    })
