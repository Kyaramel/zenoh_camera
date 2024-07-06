import cv2
import zenoh
import numpy as np
import base64


def display_frame(sample):
    """
    受信したデータを表示する関数

    引数:
    sample (Sample): Zenohから受信したサンプルデータ
    """
    if sample is None or len(sample.payload) == 0:
        return

    # 受信したデータをBase64からデコード
    jpg_as_text = sample.payload.decode("utf-8")
    jpg_original = base64.b64decode(jpg_as_text)

    # デコードしたデータをJPEGからデコード
    np_arr = np.frombuffer(jpg_original, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    resized_frame = cv2.resize(frame, (600, 480))

    print(f"frame:{resized_frame}, shape:{resized_frame.shape}")
    # フレームが有効かどうかをチェック
    if resized_frame is not None and resized_frame.size > 0:
        # フレームを表示
        cv2.imshow("Received Frame", resized_frame)
        cv2.waitKey(1)  # ウィンドウを更新


def main():
    z = zenoh.open(zenoh.Config())
    resource_path = "demo/camera"

    # 非同期でデータを受信するためのコールバックを登録
    sub = z.declare_subscriber(resource_path, display_frame)

    print("受信待機中...（終了するにはCtrl+Cを押してください）")
    try:
        while True:
            # フレームを表示
            cv2.imshow("Live Camera Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except KeyboardInterrupt:
        print("終了します...")
    finally:
        sub.close()
        z.close()


if __name__ == "__main__":
    main()
