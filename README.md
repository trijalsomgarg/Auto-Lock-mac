Auto Lock Mac 🔒

A Python project that automatically locks my Mac when I walk away from it.

It uses:
- OpenCV + MediaPipe to detect my presence through the camera.
- Bluetooth (Bleak) to check whether my iPhone is nearby.

If both sensors detect that I've left, my Mac automatically locks after 5 seconds.

SETUP

Clone the repository:

git clone YOUR_REPOSITORY_URL
cd auto-closing

Install dependencies:

pip install -r requirements.txt

FIND YOUR IPHONE ID

Run:

python find_phone_id.py

Find your iPhone in the device list and copy its ID.

Set it in your terminal:

export IPHONE_ID="YOUR_DEVICE_ID"

RUN

python auto_lock.py

Press Ctrl + C to stop.

Note: This project currently works on macOS. Your iPhone ID stays local and should never be uploaded to GitHub.