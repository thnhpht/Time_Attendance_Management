from django.shortcuts import render, redirect
import cv2
import face_recognition
import numpy as np
from django.apps import apps
from .models import Check_Out
from home import views as home_views
from . import views as check_out_views

# Create your views here.


def check_out(request):
    def find_encodings(images):
        encode_list = []
        for image in images:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(image)[0]
            encode_list.append(encode)
        return encode_list

    checked_out = []

    def save_check_out(id):
        if id not in checked_out:
            cur_user = user_model.objects.get(id=id)
            name = cur_user.name
            new_check_out = Check_Out(user_id=id, user_name=name)
            new_check_out.save()
            checked_out.append(id)

    user_model = apps.get_model('user.User')
    user = user_model.objects.all()
    id_list = []
    image_list = []

    for p in user:
        img = cv2.imread(f'./media/{p.image}')
        image_list.append(img)
        id_list.append(p.id)

    encode_list_known = find_encodings(image_list)
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
                cur_id = id_list[match_index]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, cur_id, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                save_check_out(cur_id)

        cv2.imshow('Webcam', frame)

        turn_off = False
        if cv2.waitKey(1) & 0xFF == ord('q'):
            turn_off = True
            break

    cap.release()
    cv2.destroyAllWindows()

    if turn_off:
        return redirect(home_views.home)

    return redirect(check_out_views)


