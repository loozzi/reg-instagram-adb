import base64
import os
import random
import re
import subprocess
import time
import zipfile
from typing import Dict


def adb(command: str, device_id: str = None) -> str:
    """Run an ADB command, optionally targeting a specific device.

    Example:
        >>> adb("devices")
        >>> adb("shell getprop ro.product.model", device_id="emulator-5554")
    """
    if device_id:
        cmd = f"adb -s {device_id} {command}"
    else:
        cmd = f"adb {command}"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("Lỗi:", result.stderr)
    return result.stdout


def get_devices() -> list:
    """Return all currently connected Android device IDs.

    Example:
        >>> devices = get_devices()
        >>> print(devices)
    """
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    devices = []
    for line in lines[1:]:
        if line.strip() and "device" in line:
            device_id = line.split()[0]
            devices.append(device_id)
    return devices


class File:
    __device_id: str
    __package_name: str

    def __init__(self, device_id: str, package_name: str):
        """Create a file helper bound to one device and one app package.

        Example:
            >>> f = File("emulator-5554", "com.instagram.android")
        """
        self.__device_id = device_id
        self.__package_name = package_name

    def __adb(self, command: str) -> str:
        return adb(command, self.__device_id)

    def dump_database(self, save_path: str = "."):
        """Pull the app's full SQLite database directory to the local machine.

        Example:
            >>> f = File("emulator-5554", "com.instagram.android")
            >>> f.dump_database("./dump")
        """
        db_path = f"/data/data/{self.__package_name}/databases"
        os.makedirs(save_path, exist_ok=True)
        print(f"[*] Dumping database: {self.__package_name}")  # 🐛 fix
        self.__adb(f"pull {db_path} {save_path}")
        print(f"[✓] Saved: {save_path}")

    def pull_shared_prefs(self, save_path: str = "."):
        """Pull the app's shared preferences to the local machine.

        Example:
            >>> f = File("emulator-5554", "com.instagram.android")
            >>> f.pull_shared_prefs("./dump")
        """
        prefs_path = f"/data/data/{self.__package_name}/shared_prefs"
        os.makedirs(save_path, exist_ok=True)
        print(f"[*] Dumping shared_prefs: {self.__package_name}")
        self.__adb(f"pull {prefs_path} {save_path}")
        print(f"[✓] Saved: {save_path}")

    def dump_app(self, save_path: str = "dump"):
        """Pull major app directories (db, prefs, files, cache, external) locally.

        Example:
            >>> f = File("emulator-5554", "com.instagram.android")
            >>> f.dump_app("./full_dump")
        """
        os.makedirs(save_path, exist_ok=True)
        print(f"\n[*] Bắt đầu dump: {self.__package_name}")
        print("=" * 40)

        tasks = [
            (
                "Database",
                f"/data/data/{self.__package_name}/databases",
                f"{save_path}/databases",
            ),
            (
                "Shared Prefs",
                f"/data/data/{self.__package_name}/shared_prefs",
                f"{save_path}/shared_prefs",
            ),
            ("Files", f"/data/data/{self.__package_name}/files", f"{save_path}/files"),
            ("Cache", f"/data/data/{self.__package_name}/cache", f"{save_path}/cache"),
            (
                "External",
                f"/sdcard/Android/data/{self.__package_name}",
                f"{save_path}/external",
            ),
        ]

        for name, src, dst in tasks:
            print(f"[*] Dumping {name}...")
            os.makedirs(dst, exist_ok=True)
            self.__adb(f"pull {src} {dst}")

        print("=" * 40)
        print(f"[✓] Dump xong! Lưu tại: {save_path}")


class ProxyConfig:
    def __init__(self, device_id: str):
        """Configuration for setting up a proxy on the device.

        Example:
            >>> proxy = ProxyConfig("emulator-5554")
        """
        self.__device_id = device_id

    def __adb(self, command: str) -> str:
        return adb(command, self.__device_id)

    def set_proxy(
        self, host: str, port: int, username: str = None, password: str = None
    ):
        """Set HTTP proxy for the device, with optional authentication.

        Example:
            >>> phone.set_proxy("192.168.1.5", 8080)
            >>> phone.set_proxy("192.168.1.5", 8080, username="user", password="pass")
        """

        # Proxy không có tài khoản
        if not username and not password:
            output = self.__adb(f"shell settings put global http_proxy {host}:{port}")

        # Proxy có tài khoản → format: user:pass@host:port
        else:
            output = self.__adb(
                f"shell settings put global http_proxy {username}:{password}@{host}:{port}"
            )

        if not output.strip():
            print(f"[✓] Proxy set: {host}:{port}")
        else:
            print(f"[✗] Failed: {output}")

    def clear_proxy(self):
        """Remove proxy settings from the device.

        Example:
            >>> phone.clear_proxy()
        """
        output = self.__adb("shell settings put global http_proxy :0")
        if not output.strip():
            print("[✓] Proxy cleared!")
        else:
            print(f"[✗] Failed: {output}")

    def get_proxy(self) -> str:
        """Get current proxy settings on the device.

        Example:
            >>> proxy = phone.get_proxy()
            >>> print(proxy)
        """
        output = self.__adb("shell settings get global http_proxy")
        print(f"[*] Current proxy: {output.strip()}")
        return output.strip()


class PhoneDevice:
    __device_id: str

    KEYCODE = {
        "back": 4,
        "home": 3,
        "recent": 187,
        "enter": 66,
        "delete": 67,
        "power": 26,
        "volume_up": 24,
        "volume_down": 25,
    }

    def __init__(self, device_id: str):
        """Create a phone automation helper for one connected device.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
        """
        self.__device_id = device_id
        self.files: Dict[str, File] = {}
        self.proxy_config = ProxyConfig(device_id)

    def __adb(self, command: str) -> str:
        return adb(command, self.__device_id)

    # ==========================================
    # APP MANAGEMENT
    # ==========================================

    def get_package_name_no_aapt(self, apk_path: str) -> str:
        """Extract package name from APK without aapt (pure Python).

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> pkg = phone.get_package_name_no_aapt("./app.apk")
        """
        try:
            with zipfile.ZipFile(apk_path, "r") as apk:
                with apk.open("AndroidManifest.xml") as f:
                    content = f.read()
                    matches = re.findall(
                        rb"([a-zA-Z][a-zA-Z0-9_]*(?:\.[a-zA-Z][a-zA-Z0-9_]*){2,})",
                        content,
                    )
                    for m in matches:
                        decoded = m.decode("utf-8", errors="ignore")
                        if decoded.count(".") >= 1 and not decoded.startswith(
                            "android"
                        ):
                            return decoded
        except Exception as e:
            print(f"[!] Lỗi đọc APK: {e}")
        return None

    def get_package_name(self, apk_path: str) -> str:
        """Extract the package name from an APK file using aapt (fallback to pure Python).

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> pkg = phone.get_package_name("./apk/app.apk")
        """
        result = subprocess.run(
            f"aapt dump badging {apk_path}", shell=True, capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("package:"):
                return line.split("name='")[1].split("'")[0]

        # Fallback nếu không có aapt
        print("[!] aapt không khả dụng, dùng fallback...")
        return self.get_package_name_no_aapt(apk_path)

    def install(self, apk_path: str) -> bool:
        """Install an APK file to the device.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> phone.install("./apk/app.apk")
        """
        print(f"[*] Đang cài: {apk_path}")
        output = self.__adb(f"install -r {apk_path}")

        if "Failure" in output or "failed" in output.lower():
            print("[✗] Cài đặt thất bại!")
            return False

        print("[✓] Cài đặt thành công!")
        return True

    def open(self, apk_path: str) -> bool:
        """Open an installed APK by resolving package and launchable activity.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> phone.open("./apk/app.apk")
        """
        package = self.get_package_name(apk_path)
        if not package:
            print("[!] Không lấy được package name")
            return False

        print(f"[*] Package: {package}")

        result = subprocess.run(
            f"aapt dump badging {apk_path}", shell=True, capture_output=True, text=True
        )
        activity = None
        for line in result.stdout.splitlines():
            if "launchable-activity" in line:
                activity = line.split("name='")[1].split("'")[0]
                break

        if activity:
            print(f"[*] Đang mở: {activity}")
            self.__adb(f"shell am start -n {package}/{activity}")
        else:
            print("[*] Mở app bằng monkey...")
            self.__adb(
                f"shell monkey -p {package} -c android.intent.category.LAUNCHER 1"
            )

        return True

    def install_and_open(self, apk_path: str):
        """Install an APK and launch it.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> phone.install_and_open("./apk/app.apk")
        """
        if self.install(apk_path):
            self.open(apk_path)

    def uninstall_app(self, package_name: str):
        """Uninstall an app by its package name.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> phone.uninstall_app("com.example.app")
        """
        print(f"[*] Đang gỡ: {package_name}")
        output = self.__adb(f"uninstall {package_name}")
        if "Success" in output:
            print("[✓] Gỡ thành công!")
        else:
            print("[✗] Gỡ thất bại!")

    def open_app(self, package_name: str):
        """Launch an app by package name using monkey.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> phone.open_app("com.example.app")
        """
        self.__adb(
            f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
        )

    def close_app(self, package_name: str):
        """Force-stop an app by package name.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> phone.close_app("com.example.app")
        """
        self.__adb(f"shell am force-stop {package_name}")

    def restart_app(self, package_name: str):
        """Close and reopen an app with a short wait in between.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> phone.restart_app("com.example.app")
        """
        self.close_app(package_name)  # 🐛 fix: bỏ self thừa
        time.sleep(1)
        self.open_app(package_name)  # 🐛 fix: bỏ self thừa

    def is_app_running(self, package_name: str) -> bool:
        """Check whether an app process is currently running.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> running = phone.is_app_running("com.example.app")
        """
        result = self.__adb(f"shell pidof {package_name}")  # 🐛 fix: self.__adb
        return bool(result.strip())

    def clear_app_data(self, package_name: str):
        """Clear all app data, similar to a fresh install state.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> phone.clear_app_data("com.example.app")
        """
        self.__adb(f"shell pm clear {package_name}")

    def list_packages(self, third_party_only: bool = True) -> list:
        """List installed packages on the device.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> pkgs = phone.list_packages()
        """
        flag = "-3" if third_party_only else ""
        output = self.__adb(f"shell pm list packages {flag}")
        return [
            line.replace("package:", "").strip()
            for line in output.splitlines()
            if line.startswith("package:")
        ]

    # ==========================================
    # PERMISSIONS
    # ==========================================
    def grant_permission(self, package_name: str, permission: str):
        """Grant a single permission to an app.

        Example:
            >>> phone.grant_permission("com.example.app", "android.permission.CAMERA")
        """
        output = self.__adb(f"shell pm grant {package_name} {permission}")
        if not output.strip():
            print(f"[✓] Granted: {permission}")
        else:
            print(f"[✗] Failed: {output}")

    def revoke_permission(self, package_name: str, permission: str):
        """Revoke a single permission from an app.

        Example:
            >>> phone.revoke_permission("com.example.app", "android.permission.CAMERA")
        """
        output = self.__adb(f"shell pm revoke {package_name} {permission}")
        if not output.strip():
            print(f"[✓] Revoked: {permission}")
        else:
            print(f"[✗] Failed: {output}")

    def grant_all_permissions(self, package_name: str):
        """Grant all common permissions to an app at once.

        Example:
            >>> phone.grant_all_permissions("com.example.app")
        """
        PERMISSIONS = [
            "android.permission.CAMERA",
            "android.permission.RECORD_AUDIO",
            "android.permission.READ_CONTACTS",
            "android.permission.WRITE_CONTACTS",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.READ_PHONE_STATE",
            "android.permission.CALL_PHONE",
            "android.permission.READ_CALL_LOG",
            "android.permission.SEND_SMS",
            "android.permission.READ_SMS",
            "android.permission.BLUETOOTH",
            "android.permission.BODY_SENSORS",
        ]

        print(f"[*] Granting all permissions: {package_name}")
        for perm in PERMISSIONS:
            self.grant_permission(package_name, perm)
        print(f"[✓] Done!")

    def list_permissions(self, package_name: str) -> list:
        """List all permissions (granted/denied) of an app.

        Example:
            >>> perms = phone.list_permissions("com.example.app")
        """
        output = self.__adb(f"shell dumpsys package {package_name}")

        permissions = []
        for line in output.splitlines():
            if "permission" in line.lower() and "granted=" in line.lower():
                permissions.append(line.strip())
                print(f"  {line.strip()}")

        return permissions

    # ==========================================
    # DEVICE INFO
    # ==========================================

    def get_model_name(self) -> str:
        """Return the device model name.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> model = phone.get_model_name()
        """
        return self.__adb("shell getprop ro.product.model")  # 🐛 fix: dấu chấm → space

    def get_device_info(self) -> dict:
        """Return a dict of key device properties.

        Example:
            >>> phone = PhoneDevice("emulator-5554")
            >>> info = phone.get_device_info()
        """
        props = {
            "model": "ro.product.model",
            "android_ver": "ro.build.version.release",
            "sdk": "ro.build.version.sdk",
            "brand": "ro.product.brand",
            "arch": "ro.product.cpu.abi",
        }
        info = {}
        for key, prop in props.items():
            info[key] = self.__adb(f"shell getprop {prop}").strip()
        return info

    # ==========================================
    # INPUT
    # ==========================================

    def tap(self, x: int, y: int):
        """Tap once at screen coordinates (x, y).

        Example:
            >>> phone.tap(540, 1200)
        """
        self.__adb(f"shell input tap {x} {y}")

    def long_press(self, x: int, y: int, duration_ms: int = 1000):
        """Long press at screen coordinates.

        Example:
            >>> phone.long_press(540, 1200, duration_ms=1500)
        """
        self.__adb(f"shell input swipe {x} {y} {x} {y} {duration_ms}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300):
        """Swipe from (x1, y1) to (x2, y2).

        Example:
            >>> phone.swipe(500, 1500, 500, 300)
        """
        self.__adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration_ms}")

    def scroll_down(self, duration_ms: int = 300):
        """Scroll down the screen.

        Example:
            >>> phone.scroll_down()
        """
        self.__adb(f"shell input swipe 540 1200 540 400 {duration_ms}")

    def scroll_up(self, duration_ms: int = 300):
        """Scroll up the screen.

        Example:
            >>> phone.scroll_up()
        """
        self.__adb(f"shell input swipe 540 400 540 1200 {duration_ms}")

    def press_key(self, keycode: int):
        """Send a key event to the device.

        Example:
            >>> phone.press_key(PhoneDevice.KEYCODE["home"])
        """
        self.__adb(f"shell input keyevent {keycode}")

    def input_text(self, text: str, delay: float = 0.1):
        """Input text one character at a time with randomized delay.

        Example:
            >>> phone.input_text("hello world", delay=0.08)
        """
        text = text.replace(" ", "%s")
        for char in text:
            self.__adb(f"shell input text '{char}'")
            time.sleep(delay + random.uniform(-0.03, 0.03))

    def input_text_unicode(self, text: str):
        """Input Unicode text via ADB Keyboard broadcast.

        Example:
            >>> phone.input_text_unicode("Xin chào")
        """
        encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        self.__adb(f"shell am broadcast -a ADB_INPUT_B64 --es msg '{encoded}'")

    # ==========================================
    # SCREEN
    # ==========================================

    def screenshot(self, save_path: str = "screen.png"):
        """Capture a screenshot and save it locally.

        Example:
            >>> phone.screenshot("./screen.png")
        """
        self.__adb(f"shell screencap /sdcard/_screen.png")
        self.__adb(f"pull /sdcard/_screen.png {save_path}")
        self.__adb(f"shell rm /sdcard/_screen.png")
        print(f"[✓] Saved: {save_path}")

    def _enable_pointer_location(self):
        """Enable pointer location overlay for touch debugging."""
        self.__adb("shell settings put system pointer_location 1")

    def _disable_pointer_location(self):
        """Disable pointer location overlay."""
        self.__adb("shell settings put system pointer_location 0")

    # ==========================================
    # FILE & FOLDER
    # ==========================================

    def pull_folder(self, device_path: str, save_path: str = "."):
        """Pull a folder from the device locally.

        Example:
            >>> phone.pull_folder("/sdcard/DCIM", "./backup")
        """
        os.makedirs(save_path, exist_ok=True)
        print(f"[*] Đang dump: {device_path} → {save_path}")
        self.__adb(f"pull {device_path} {save_path}")
        print(f"[✓] Xong!")

    def push_file(self, local_path: str, device_path: str):
        """Push a local file to the device.

        Example:
            >>> phone.push_file("./config.txt", "/sdcard/config.txt")
        """
        self.__adb(f"push {local_path} {device_path}")

    def list_files(self, device_path: str) -> list:
        """List files in a device directory.

        Example:
            >>> phone.list_files("/sdcard/Download")
        """
        output = self.__adb(f"shell ls -la {device_path}")
        return [line for line in output.splitlines() if line.strip()]

    def read_file(self, device_path: str) -> str:
        """Read a text file on the device without pulling it.

        Example:
            >>> content = phone.read_file("/sdcard/sample.txt")
        """
        return self.__adb(f"shell cat {device_path}")

    def find_file(self, filename: str, search_path: str = "/sdcard") -> list:
        """Find files by partial name on the device.

        Example:
            >>> phone.find_file(".json", "/sdcard")
        """
        output = self.__adb(
            f"shell find {search_path} -name '*{filename}*' 2>/dev/null"
        )
        results = [line for line in output.splitlines() if line.strip()]
        print(f"[*] Tìm thấy {len(results)} file:")
        for f in results:
            print(f"    {f}")
        return results

    def grep_file(self, keyword: str, search_path: str = "/sdcard") -> str:
        """Search for a keyword inside files on the device.

        Example:
            >>> phone.grep_file("token", "/sdcard")
        """
        return self.__adb(f"shell grep -r '{keyword}' {search_path} 2>/dev/null")

    def delete_file(self, device_path: str):
        """Delete a file on the device.

        Example:
            >>> phone.delete_file("/sdcard/tmp.txt")
        """
        self.__adb(f"shell rm -f {device_path}")

    # ==========================================
    # UTILITY
    # ==========================================

    def wait(self, seconds: float, randomize: bool = True):
        """Sleep for a duration with optional random jitter.

        Example:
            >>> phone.wait(1.5)
        """
        if randomize:
            seconds += random.uniform(-0.1, 0.1)
        time.sleep(max(0, seconds))

    def get_logcat(self, package_name: str, lines: int = 50) -> str:
        """Capture recent logcat output filtered by package name.

        Example:
            >>> logs = phone.get_logcat("com.example.app", lines=100)
        """
        result = subprocess.run(
            f"adb -s {self.__device_id} logcat -d -t {lines}",
            shell=True,
            capture_output=True,
            text=True,
        )
        filtered = [line for line in result.stdout.splitlines() if package_name in line]
        return "\n".join(filtered)

    def connect(self, host: str, port: int = 5555) -> bool:
        """Connect to a device over WiFi (ADB wireless).

        Example:
            >>> phone = PhoneDevice("192.168.1.100:5555")
            >>> phone.connect("192.168.1.100", 5555)
        """
        output = adb(f"connect {host}:{port}")
        return "connected" in output.lower()

    def disconnect(self):
        """Disconnect this device from ADB.

        Example:
            >>> phone.disconnect()
        """
        adb(f"disconnect {self.__device_id}")
