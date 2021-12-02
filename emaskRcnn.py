import cv2
import numpy as np

try:
    net = cv2.dnn.readNetFromTensorflow(
        "dnn/frozen_inference_graph_coco.pb",
        "dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt",
    )
except Exception as err:
    print(err)


def loadImage(images):
    img = np.array(images.convert("RGB"))
    return img


def maskImage(images):
    colors = np.random.randint(0, 255, (80, 3))
    img = loadImage(images)
    height, width, _ = img.shape

    # Create black image
    black_image = np.zeros((height, width, 3), np.uint8)
    black_image[:] = (100, 100, 0)

    blob = cv2.dnn.blobFromImage(img, swapRB=True)

    net.setInput(blob)
    boxes, masks = net.forward(["detection_out_final", "detection_masks"])
    total_object = boxes.shape[2]

    for i in range(total_object):
        box = boxes[0, 0, i]
        obj_class = box[1]
        score = box[2]
        if score < 0.7:
            continue

        # Box Coordinate
        x = int(box[3] * width)
        y = int(box[4] * height)
        x2 = int(box[5] * width)
        y2 = int(box[6] * height)

        roi = black_image[y:y2, x:x2]
        roi_height, roi_width, _ = roi.shape

        # Get the masks
        mask = masks[i, int(obj_class)]
        mask = cv2.resize(mask, (roi_width, roi_height))
        _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)

        cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 3)

        # Get mask coordinates
        countours, _ = cv2.findContours(
            np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        color = colors[int(obj_class)]
        for cnt in countours:
            cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

    return img, black_image
