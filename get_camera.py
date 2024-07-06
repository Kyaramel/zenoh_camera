import cv2
import zenoh
import numpy as np
import base64

image = None


def display_frame(sample):
    """
    受信したデータを表示する関数

    引数:
    sample (Sample): Zenohから受信したサンプルデータ
    """
    global image
    if sample is None or len(sample.payload) == 0:
        return

    # 受信したデータをBase64からデコード
    jpg_as_text = sample.payload.decode("utf-8")
    jpg_original = base64.b64decode(jpg_as_text)

    # デコードしたデータをJPEGからデコード
    np_arr = np.frombuffer(jpg_original, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    resized_frame = cv2.resize(frame, (600, 480))

    image = resized_frame


def main():
    global image
    z = zenoh.open(zenoh.Config())
    resource_path = "demo/camera"

    # 非同期でデータを受信するためのコールバックを登録
    sub = z.declare_subscriber(resource_path, display_frame)

    print("受信待機中...（終了するにはCtrl+Cを押してください）")
    try:
        while True:
            # フレームを表示
            if image is not None and image.size > 0:
                cv2.imshow("Live Camera Feed", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except Exception as e:
        print(e)
        print("終了します...")
    finally:
        z.close()


if __name__ == "__main__":
    main()
