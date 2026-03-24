"""Practical usage examples for lib.py.

Run:
	python examples.py

You can modify DEVICE_ID and PACKAGE_NAME below to match your environment.
"""

from lib import adb, get_devices, File, PhoneDevice


# Update these values for your setup.
DEVICE_ID = "emulator-5554"
PACKAGE_NAME = "com.instagram.android"
APK_PATH = "./apk/app.apk"


def example_basic_adb() -> None:
	"""Example 1: Basic ADB helpers."""
	print("\n=== Example 1: basic adb ===")
	adb("devices")

	devices = get_devices()
	print("Connected devices:", devices)

	if devices:
		model = adb("shell getprop ro.product.model", device_id=devices[0]).strip()
		print("First device model:", model)


def example_phone_device() -> None:
	"""Example 2: PhoneDevice automation flow."""
	print("\n=== Example 2: phone automation ===")
	phone = PhoneDevice(DEVICE_ID)

	print("Model:", phone.get_model_name().strip())
	print("Device info:", phone.get_device_info())

	# App lifecycle
	phone.open_app(PACKAGE_NAME)
	phone.wait(1.5)
	print("Is app running:", phone.is_app_running(PACKAGE_NAME))

	# Basic input
	phone.tap(540, 1200)
	phone.wait(0.5)
	phone.input_text("hello from adb")
	phone.press_key(PhoneDevice.KEYCODE["enter"])

	# Screen and file actions
	phone.screenshot("./screen.png")
	print("Files in /sdcard/Download:", phone.list_files("/sdcard/Download")[:5])
	print("Find *.json under /sdcard:", phone.find_file(".json", "/sdcard")[:5])


def example_file_dump() -> None:
	"""Example 3: Pull app data folders with File helper."""
	print("\n=== Example 3: file dump ===")
	f = File(DEVICE_ID, PACKAGE_NAME)

	# These often require proper permissions/root depending on device.
	f.dump_database("./dump/databases")
	f.pull_shared_prefs("./dump/shared_prefs")
	f.dump_app("./dump/full_app")


def example_apk_install() -> None:
	"""Example 4: APK parsing/install flow."""
	print("\n=== Example 4: apk install ===")
	phone = PhoneDevice(DEVICE_ID)

	pkg = phone.get_package_name(APK_PATH)
	print("Package from APK:", pkg)

	# Uncomment this line when you want to install and open the APK.
	# phone.install_and_open(APK_PATH)


if __name__ == "__main__":
	# Run examples one by one as needed.
	example_basic_adb()
	example_phone_device()
	# example_file_dump()
	# example_apk_install()

