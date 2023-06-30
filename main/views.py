from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
import cv2
import face_recognition
import numpy as np
from .models import Check_In, Check_Out, Config
from datetime import timedelta, datetime
import datetime as dt
import time
import calendar
from dateutil.relativedelta import relativedelta
from geopy.geocoders import Nominatim
from geopy.distance import distance
import subprocess
from .forms import ConfigForm
import winsdk.windows.devices.geolocation as wdg, asyncio
from django.template.loader import get_template


User = get_user_model()
geolocator = Nominatim(user_agent="thnhpht")


@login_required(login_url='sign_in')
def home(request):
    if not request.user.is_authenticated:
        return redirect('/sign-in/')
    return render(request, './staff/home.html')


def adminHome(request):
    if not request.user.is_authenticated:
        return redirect('/sign-in/')
    return render(request, './admin/home.html')


def authenticateUser(email=None, password=None):
    try:
        user = User.objects.get(email=email)

        if check_password(password, user.password):
            return user
        return None
    except User.DoesNotExist:
        return None


def signIn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticateUser(email, password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Đăng nhập thành công')
            return redirect('/home/')
        else:
            messages.warning(request, 'Email hoặc mật khẩu không chính xác')
    return render(request, './auth/sign-in.html')


def signUp(request):
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
    return render(request, './auth/sign-up.html')


def signOut(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công')
    return redirect('/sign-in/')


def staff(request):
    return render(request, './staff/staff.html')


def manageStaff(request):
    if request.method == "POST":
        search = request.POST.get('search')
        users = User.objects.filter(name__contains=search)
    else:
        users = User.objects.all()
    return render(request, './admin/manage/manage-staff.html', {
        'users': users,
    })


def findEncodings(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(image)
    return encode


async def getCoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]


def getLoc():
    return asyncio.run(getCoords())


# Kiểm tra địa chỉ chấm công
def checkLocation(request):
    try:
        config = Config.objects.all()[:1].get()

        current_location = (float(getLoc()[0]), float(getLoc()[1]))
        company_location = (float(config.lat), float(config.lon))

        if distance(current_location, company_location).km > 0.5:
            messages.warning(request, 'Địa điểm chấm công không hợp lệ')
            return redirect('/home/')

    except Exception as e:
        messages.warning(request, e)
        return redirect('/home/')


def checkWifi(request):
    try:
        wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
        data = wifi.decode('utf-8')
        data = data.split('SSID')
        data = data[1].split('\n')
        data = data[0].split(': ')
        data = data[1].strip()
        config = Config.objects.get(wifi=data)
    except Exception as e:
        messages.warning(request, 'Wifi chấm công không hợp lệ')
        return redirect('/home/')


def checkIn(request):
    checkLocation(request)
    checkWifi(request)
    current = datetime.now()
    # Kiểm tra User đã chấm công vào chưa
    try:
        Check_In.objects.get(date=current.date())
        messages.warning(request, 'Nhân viên đã chấm công vào')
        return redirect('/home/')
    except:
        pass

    def saveTimekeeping():
        timekeeping = Check_In(user_id=request.user.id)
        timekeeping.save()
        messages.success(request, 'Chấm công vào thành công')

    image = cv2.imread(f'./media/{request.user.image}')
    encode_list_known = findEncodings(image)

    for i in range(5):
        try:
            cap = cv2.VideoCapture(0)
            break
        except:
            continue

    if not (cap.isOpened()):
        messages.warning(request, 'Không thể mở camera trên thiết bị')
        return redirect('/home/')

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
                saveTimekeeping()
                checked = True

        window_name = "Webcam"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

        turn_off = False
        if checked or cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE) < 1:
            turn_off = True
            time.sleep(2)
            cv2.destroyAllWindows()
            cap.release()
            break

    if turn_off:
        return redirect('/home/')
    return render(request, './staff/check-in.html')


def checkOut(request):
    checkLocation(request)
    checkWifi(request)
    current = datetime.now()

    # Kiểm tra User đã chấm công vào chưa
    try:
        Check_In.objects.get(date=current.date())
    except:
        messages.warning(request, 'Nhân viên chưa chấm công vào')
        return redirect('/home/')

    # Kiểm tra User đã chấm công ra chưa
    try:
        Check_Out.objects.get(date=current.date())
        messages.warning(request, 'Nhân viên đã chấm công ra')
        return redirect('/home/')
    except:
        pass

    def saveTimekeeping():
        timekeeping = Check_Out(user_id=request.user.id)
        timekeeping.save()
        messages.success(request, 'Chấm công ra thành công')

    image = cv2.imread(f'./media/{request.user.image}')
    encode_list_known = findEncodings(image)

    for i in range(5):
        try:
            cap = cv2.VideoCapture(i)
            break
        except:
            continue

    if not (cap.isOpened()):
        messages.warning(request, 'Không thể mở camera trên thiết bị')
        return redirect('/home/')

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
                saveTimekeeping()
                checked = True

        window_name = "Webcam"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

        turn_off = False
        if checked or cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE) < 1:
            turn_off = True
            time.sleep(2)
            cv2.destroyAllWindows()
            cap.release()
            break

    if turn_off:
        return redirect('/home/')
    return render(request, './staff/check-out.html')


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

    return render(request, './staff/timesheets.html', {
        'list_time_stamp': list_time_stamp,
    })


def getDate(date_from, date_to):
    arr_datetime = []
    current = date_from
    arr_datetime.append(current)

    while current < date_to:
        current += timedelta(days=1)
        if current.strftime("%A") != "Sunday":
            arr_datetime.append(current)
    return arr_datetime


def statistic(request):
    current = datetime.now()

    if request.method == "POST":
        month = int(request.POST.get('month'))
        current = datetime(current.year, int(month), 1)
        date_from = dt.date(2023, month, 1)
        date_to = date_from + relativedelta(months=+1) - timedelta(days=1)
    else:
        month = current.month
        date_from = dt.date(2023, month, 1)
        date_to = dt.date.today()

    date = getDate(date_from, date_to)
    count_worktime = 0
    days_in_month = int(calendar.monthrange(current.year, month)[1])
    all_worktime_user = Check_In.objects.filter(user_id=request.user.id)

    for day in all_worktime_user:
        if day.date.month == month:
            count_worktime += 1

    count_absent = len(date) - count_worktime

    return render(request, './staff/statistic.html', {
        'month': month,
        'count_worktime': count_worktime,
        'count_absent': count_absent,
    })


def config(request):
    configs = Config.objects.all()
    add_button = False
    if len(configs) == 0:
        add_button = True

    return render(request, './admin/config/config.html', {
        'configs': configs,
        'add_button' : add_button,
    })


def createConfig(request):
    form = ConfigForm()
    configs = Config.objects.all()

    if request.method == "POST":
        location = request.POST.get('location_add')
        wifi = request.POST.get('wifi')

        try:
            location_detail = geolocator.geocode(location, addressdetails=True)
            lat = location_detail.raw['lat']
            lon = location_detail.raw['lon']

            new_config = Config(location_add=location, lat=lat, lon=lon, wifi=wifi)
            new_config.save()

            messages.success(request, 'Thêm cấu hình chấm công thành công')
            return redirect('config')
        except:
            messages.warning(request, 'Địa điểm không hợp lệ')

    return render(request, './admin/config/create-config.html', {
        'configs': configs,
        'form': form,
    })


def updateConfig(request, pk):
    configs = Config.objects.all()
    config = Config.objects.get(id=pk)
    form = ConfigForm(instance=config)
    if request.method == "POST":
        location = request.POST.get('location_add')
        wifi = request.POST.get('wifi')

        try:
            location_detail = geolocator.geocode(location, addressdetails=True)
            lat = location_detail.raw['lat']
            lon = location_detail.raw['lon']

            config.location_add = location
            config.lat = lat
            config.lon = lon
            config.wifi = wifi
            config.save()
            messages.success(request, 'Chỉnh sửa cấu hình chấm công thành công')
            return redirect('config')
        except:
            messages.warning(request, 'Địa điểm không hợp lệ')

    return render(request, './admin/config/update-config.html', {
        'configs': configs,
        'form': form,
    })


def deleteConfig(request, pk):
    configs = Config.objects.all()
    config = Config.objects.get(id=pk)
    if request.method == "POST":
        config.delete()
        messages.success(request, 'Xóa cấu hình chấm công thành công')
        return redirect('config')
    return render(request, './admin/config/delete-config.html', {
        'configs': configs,
    })
