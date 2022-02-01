import cv2
from modules import components


class Detection:
    def __init__(self, st):
        self.st = st

        self.face_cascade = cv2.CascadeClassifier(
            "haarcascade/haarcascade_frontalface_default.xml"
        )
        self.smile_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_smile.xml")
        self.eye_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_eye.xml")
        self.component = components.Components(self.st)

    def detectFaces(self, images):
        new_img = self.component.cvtImgToArr(images)
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect Faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 4)
        return img, faces

    def detectSmiles(self, images):
        new_img = self.component.cvtImgToArr(images)
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            the_face = img[y : y + h, x : x + w]
            face_gray_scale = cv2.cvtColor(the_face, cv2.COLOR_BGR2GRAY)
            smile_detect = self.smile_cascade.detectMultiScale(
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

    def detectEye(self, images):
        new_img = self.component.cvtImgToArr(images)
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        eyes = self.eye_cascade.detectMultiScale(gray, minSize=(20, 20))

        if len(eyes) != 0:
            for (x, y, w, h) in eyes:
                cv2.rectangle(img, (x, y), (x + h, y + w), (0, 255, 0))

        return img
