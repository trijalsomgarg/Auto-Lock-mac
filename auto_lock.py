import threading
import time
import cv2
import mediapipe as mp
import asyncio
import os

face_detected = False
phone_nearby = False
camera_working = False
bluetooth_working = False
stop_event = threading.Event()
IPHONE_ID = os.environ.get("IPHONE_ID")
if not IPHONE_ID:
        raise SystemExit(
            "Phone ID missing! \n"
            "Run: export IPHONE_ID='YOUR_DEVICE_ID'"
        )
# locking 
def lock_mac():
    print("🔒 Locking Mac...")
    os.system("pmset displaysleepnow")
#    camera
def camera():
    global face_detected
    global camera_working

    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision

    base_options = python.BaseOptions(
        model_asset_path="models/blaze_face_short_range.tflite",
        delegate=python.BaseOptions.Delegate.CPU
    )

    options = vision.FaceDetectorOptions(
        base_options=base_options
    )

    detector = vision.FaceDetector.create_from_options(options)

    cap = cv2.VideoCapture(1)

    while not stop_event.is_set():
        ret, frame = cap.read()

        if not ret:
            camera_working = False
            break
        camera_working = True    
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        detection_result = detector.detect(mp_image)

        face_detected = False

        for detection in detection_result.detections:
            score = detection.categories[0].score

            if score >= 0.5:
                face_detected = True
                break

        

    cap.release()

# blutooth
def bluetooth():
    global phone_nearby
    global bluetooth_working 

    from bleak import BleakScanner
    

    

    PHONE_TIMEOUT = 5
    last_seen = None
    RSSI_THRESHOLD = -69

    def device_detected(device, advertisement):
        nonlocal last_seen

        if device.address == IPHONE_ID:
            # print("RSSI:", advertisement.rssi)
            if advertisement.rssi >= RSSI_THRESHOLD:
                last_seen = time.time()
            # print("📱 iPhone detected")

    async def scan():
        global phone_nearby
        global bluetooth_working

        scanner = BleakScanner(
            detection_callback=device_detected
        )

        await scanner.start()
        bluetooth_working = True

        while not stop_event.is_set():
            if last_seen is None:
                phone_nearby = False
            else:
                time_since_seen = time.time() - last_seen
                phone_nearby = time_since_seen < PHONE_TIMEOUT

            await asyncio.sleep(1)
        await scanner.stop()
        bluetooth_working = False

    asyncio.run(scan())

camera_thread = threading.Thread(target=camera)
bluetooth_thread = threading.Thread(target=bluetooth)

camera_thread.start()
bluetooth_thread.start()

left_since = None
user_left = False

try:
    while not stop_event.is_set():

        if not camera_working or not bluetooth_working:
            print("Sensor unavailable")
            left_since = None
            user_left = False

        # Both sensors say the user is present
        elif face_detected and phone_nearby:
            print("User present")
            left_since = None
            user_left = False

        # Both sensors say the user is absent
        elif not face_detected and not phone_nearby:
            print("User possibly left")

            if left_since is None:
                left_since = time.time()

            if time.time() - left_since >= 5 and not user_left:
                print("User has left!")
                user_left = True
                lock_mac()

        # Sensors disagree
        else:
            print("Sensors disagree")
            left_since = None

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping...")
    stop_event.set()

camera_thread.join()
bluetooth_thread.join()

print("Program stopped.")