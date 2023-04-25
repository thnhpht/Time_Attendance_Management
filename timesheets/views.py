from django.shortcuts import render
from check_in.models import Check_In
from check_out.models import Check_Out
from datetime import timedelta


# Create your views here.

def timesheets(request):
    check_in = Check_In.objects.all()
    check_out = Check_Out.objects.all()
    list_time_stamp = {}

    for ci in check_in:
        try:
            co = Check_Out.objects.get(date=ci.date)
            time_co = co.time.strftime("%H:%M:%S")
            t1 = timedelta(hours=ci.time.hour, minutes=ci.time.minute, seconds=ci.time.second)
            t2 = timedelta(hours=co.time.hour, minutes=co.time.minute, seconds=co.time.second)
            work_time = t2 - t1
        except:
            time_co = ""
            work_time = ""

        list_time_stamp.update({ci.date.strftime("%d/%m/%Y"): [ci.personnel_id, ci.personnel_name,
                                                               ci.time.strftime("%H:%M:%S"), time_co, work_time]})

    return render(request, 'timesheets.html', {
        'check_in': check_in,
        'check_out': check_out,
        'list_time_stamp': list_time_stamp,
    })
