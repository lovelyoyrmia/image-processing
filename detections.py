import cv2
import numpy as np

try:
    face_cascade = cv2.CascadeClassifier(
       "haarcascade/haarcascade_frontalface_default.xml"
    )
    smile_cascade = cv2.CascadeClassifier(
       "haarcascade/haarcascade_smile.xml"
    )
except Exception as err:
    print(err)


def detect_faces(images):
    global face_cascade, smile_cascade
    new_img = np.array(images.convert("RGB"))
    img = cv2.cvtColor(new_img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect Faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 4)
    return img, faces


def detect_smiles(images):
    new_img = np.array(images.convert("RGB"))
    img = cv2.cvtColor(new_img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        the_face = img[y : y + h, x : x + w]
        face_gray_scale = cv2.cvtColor(the_face, cv2.COLOR_BGR2GRAY)
        smile_detect = smile_cascade.detectMultiScale(
            face_gray_scale, 1.2, minNeighbors=25
        )

        if len(smile_detect) > 0:
            cv2.putText(
                img,
                "smiling",
                (x, y + h + 40),
                fontScale=3,
                fontFace=cv2.FONT_HERSHEY_PLAIN,
                color=(255, 0, 0),
                thickness=4,
            )
        else:
            cv2.putText(
                img,
                "not smiling :(",
                (x, y + h + 40),
                fontScale=3,
                fontFace=cv2.FONT_HERSHEY_PLAIN,
                color=(255, 0, 0),
                thickness=4,
            )

    return img
