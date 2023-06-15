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
from datetime import timedelta, datetime
import time

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
                return redirect('/sign-in/')
            else:
                messages.warning(request, 'Mật khẩu và mật khẩu xác nhận khác nhau')
    return render(request, 'sign-up.html')


def sign_out(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công')
    return redirect('/sign-in/')


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
        current = datetime.now()
        try:
            Check_In.objects.get(date=current.date())
            messages.warning(request, 'Không thể chấm công do nhân viên đã chấm công vào')
        except:
            timekeeping = Check_In(user_id=request.user.id)
            timekeeping.save()
            messages.success(request, 'Chấm công vào thành công')


    image = cv2.imread(f'./media/{request.user.image}')
    encode_list_known = find_encodings(image)

    for i in range(5):
        try:
            cap = cv2.VideoCapture(i)
            break
        except:
            continue

    checked = False

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

            if face_dis[match_index] < 0.45:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, "Cham cong vao thanh cong", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)
                save_timekeeping()
                checked = True

        window_name = "Webcam"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

        if checked:
            time.sleep(2)
            cv2.destroyAllWindows()
            cap.release()
            break

    if checked:
        return redirect('/home/')
    return render(request, 'check-in.html')


def check_out(request):
    def save_timekeeping():
        current = datetime.now()
        try:
            Check_Out.objects.get(date=current.date())
            messages.warning(request, 'Không thể chấm công do nhân viên đã chấm công ra')
        except:
            timekeeping = Check_Out(user_id=request.user.id)
            timekeeping.save()
            messages.success(request, 'Chấm công ra thành công')

    image = cv2.imread(f'./media/{request.user.image}')
    encode_list_known = find_encodings(image)

    for i in range(5):
        try:
            cap = cv2.VideoCapture(i)
            break
        except:
            continue

    checked = False

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

            if face_dis[match_index] < 0.45:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, "Cham cong ra thanh cong", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)
                save_timekeeping()
                checked = True

        window_name = "Webcam"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

        if checked:
            time.sleep(2)
            cv2.destroyAllWindows()
            cap.release()
            break

    if checked:
        return redirect('/home/')
    return render(request, 'check-out.html')


def timesheets(request):
    days_in_week = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    list_time_stamp = {}

    if request.session.get('now'):
        day, month, year = request.session.get('now').split("/")
        now = datetime(int(year), int(month), int(day))
    else:
        now = datetime.now()

    if request.method == "POST":
        if 'current-week' in request.POST:
            now = datetime.now()
        elif 'previous-week' in request.POST:
            now = now - timedelta(days=now.weekday() + 1)
        elif 'next-week' in request.POST:
            now = now - timedelta(days=now.weekday() - 8)
        else:
            date = request.POST.get('date')
            month, day, year = date.split("/")
            now = datetime(int(year), int(month), int(day))

        request.session['now'] = str(now.day) + "/" + str(now.month) + "/" + str(now.year)

    for i in range(7):
        current = now - timedelta(days=now.weekday() - i)
        day = current.date().strftime("%d/%m/%Y")

        try:
            ci = Check_In.objects.get(user_id=request.user.id, date=current.date())
            time_ci = ci.time.strftime("%H:%M:%S")
        except:
            ci = ""
            time_ci = ""

        try:
            co = Check_Out.objects.get(user_id=request.user.id, date=current.date())
            time_co = co.time.strftime("%H:%M:%S")
        except:
            co = ""
            time_co = ""

        try:
            work_time = timedelta(hours=co.time.hour, minutes=co.time.minute, seconds=co.time.second) - timedelta(
                hours=ci.time.hour, minutes=ci.time.minute, seconds=ci.time.second)
        except:
            work_time = ""

        list_time_stamp.update({days_in_week[i]: [day, time_ci, time_co, work_time]})

    return render(request, 'timesheets.html', {
        'check_in': check_in,
        'check_out': check_out,
        'list_time_stamp': list_time_stamp,
    })
