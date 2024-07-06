import cv2
import zenoh
import base64
import time


def capture_and_publish(cam_index, zenoh_session, resource_path):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print("カメラが開けません")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("フレームを取得できません")
            break

        # フレームをJPEG形式にエンコード
        _, buffer = cv2.imencode(".jpg", frame)
        jpg_as_text = base64.b64encode(buffer).decode("utf-8")

        # Zenohを使用してフレームを送信
        zenoh_session.put(resource_path, jpg_as_text)

        # 表示 (オプション)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    z = zenoh.open(zenoh.Config())
    resource_path = "demo/camera"
    capture_and_publish(0, z, resource_path)
    z.close()


if __name__ == "__main__":
    main()
