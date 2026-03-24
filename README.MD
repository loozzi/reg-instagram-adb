# reg-instagram-adb

Python toolkit for Android automation over ADB, focused on supporting Instagram account creation/testing flows on a real device or emulator.

## Key points

- This project is built for testing and automation research purposes.
- Community contributions are welcome.

## What this project does

- Connects to Android devices with ADB.
- Automates touch/input actions (tap, swipe, key events, text input).
- Opens/closes apps and checks app running status.
- Installs APK files and extracts package names.
- Captures screenshots and performs basic file operations on device storage.
- Dumps app data folders (database, shared preferences, files, cache).

## Main files

- `lib.py`: core automation library (`adb`, `get_devices`, `PhoneDevice`, `File`).
- `examples.py`: runnable examples of common workflows.
- `apk/`: place APK files here if you want to install/test them.

## Requirements

- Python 3.9+
- Android ADB available in PATH (or bundled in this repo environment)
- Android device/emulator with USB debugging enabled
- (Optional) `aapt` for reliable APK metadata parsing

## Quick start

1. Verify device connection:

```bash
adb devices
```

2. Run the example script:

```bash
python examples.py
```

3. Edit these values in `examples.py` to match your setup:

- `DEVICE_ID`
- `PACKAGE_NAME`
- `APK_PATH`

## Usage example

```python
from lib import get_devices, PhoneDevice

devices = get_devices()
if not devices:
		raise RuntimeError("No Android device connected")

phone = PhoneDevice(devices[0])

# Open Instagram
phone.open_app("com.instagram.android")
phone.wait(2)

# Example interactions
phone.tap(540, 1700)  # tap sign-up area (coordinates depend on device)
phone.input_text("testuser123")
phone.press_key(PhoneDevice.KEYCODE["enter"])
phone.screenshot("./signup-step.png")
```

## Instagram account creation flow (ADB automation)

You can build a step-by-step script with `PhoneDevice` methods:

1. Open Instagram with `open_app()`.
2. Tap the sign-up UI elements using `tap()`.
3. Fill fields with `input_text()` or `input_text_unicode()`.
4. Navigate between fields using `press_key()`.
5. Swipe when needed using `swipe()`.
6. Save checkpoints with `screenshot()`.
7. Validate app state with `is_app_running()`.

Note:
- UI coordinates vary by screen size and Instagram app version.
- Add `wait()` calls between actions to improve stability.
- Prefer testing on your own accounts/devices and follow platform Terms of Service.

## Extra operations

- App data dump:
	- `File(device_id, package).dump_database()`
	- `File(device_id, package).pull_shared_prefs()`
	- `File(device_id, package).dump_app()`
- Device file handling:
	- `phone.list_files(path)`
	- `phone.read_file(path)`
	- `phone.find_file(name, search_path)`
	- `phone.pull_folder(device_path, save_path)`

## Troubleshooting

- `device unauthorized`:
	- Reconnect USB and allow debugging prompt on device.
- `no devices/emulators found`:
	- Check cable, enable Developer options + USB debugging, rerun `adb devices`.
- Cannot dump `/data/data/...`:
	- Some paths require root/debuggable app permissions.
- `aapt` not found:
	- Keep using fallback package extraction (`get_package_name_no_aapt`), or install `aapt`.

## Safety and responsibility

Use this project for legitimate testing/automation on systems and accounts you are authorized to use.

## Contributing

Contributions from the community are welcome, including bug fixes, code improvements, documentation updates, and new examples.

