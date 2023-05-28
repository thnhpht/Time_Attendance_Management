from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
import cv2
import face_recognition
import numpy as np
from .models import Check_In
from .models import Check_Out

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
    user = User.objects.get(id=request.user.id)
    return render(request, 'user.html', {
        'user': user,
    })


def staff(request):
    users = User.objects.all()
    return render(request, 'staff.html', {
        'users': users,
    })


def find_encodings(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(image)
    return encode


def check_in(request):
    def save_timekeeping():
        timekeeping = Check_In(user_id=request.user.id, user_name=request.user.name)
        timekeeping.save()

    image = cv2.imread(f'./media/{request.user.image}')
    encode_list_known = find_encodings(image)
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        img_size = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        img_size = cv2.cvtColor(img_size, cv2.COLOR_BGR2RGB)

        faces_cur_frame = face_recognition.face_locations(img_size)
        encodes_cur_frame = face_recognition.face_encodings(img_size, faces_cur_frame)

        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            matches = face_recognition.compare_faces(encode_list_known, encodeFace)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            match_index = np.argmin(face_dis)

            if matches[match_index]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, "Chấm công vào thành công", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)
                save_timekeeping()

        cv2.imshow('Webcam', frame)

        turn_off = False
        if cv2.waitKey(1) & 0xFF == ord('q'):
            turn_off = True
            break

    cap.release()
    cv2.destroyAllWindows()

    if turn_off:
        return redirect('/home/')
    return redirect('/check-in/')


def check_out(request):
    def save_timekeeping():
        timekeeping = Check_Out(user_id=request.user.id, user_name=request.user.name)
        timekeeping.save()

    image = cv2.imread(f'./media/{request.user.image}')
    encode_list_known = find_encodings(image)
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        img_size = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        img_size = cv2.cvtColor(img_size, cv2.COLOR_BGR2RGB)

        faces_cur_frame = face_recognition.face_locations(img_size)
        encodes_cur_frame = face_recognition.face_encodings(img_size, faces_cur_frame)

        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            matches = face_recognition.compare_faces(encode_list_known, encodeFace)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            match_index = np.argmin(face_dis)

            if matches[match_index]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, "Chấm công ra thành công", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)
                save_timekeeping()

        cv2.imshow('Webcam', frame)

        turn_off = False
        if cv2.waitKey(1) & 0xFF == ord('q'):
            turn_off = True
            break

    cap.release()
    cv2.destroyAllWindows()

    if turn_off:
        return redirect('/home/')
    return redirect('/check-out/')
