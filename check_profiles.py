import re
import subprocess
from datetime import datetime


def run_adb(cmd):
    try:
        result = (
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            .decode("utf-8")
            .strip()
        )
        return result if result else "Không lấy được"
    except:
        return "Lỗi (kiểm tra ADB hoặc quyền)"


print("=" * 60)
print("🔍 KIỂM TRA THÔNG SỐ SAMSUNG S8 - ANDROID 9")
print(f"Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print("=" * 60)

# ==================== BUILD PROPERTIES ====================
print("\n📱 1. BUILD PROPERTIES (quan trọng nhất)")
props = [
    "ro.product.manufacturer",
    "ro.product.model",
    "ro.product.device",
    "ro.product.brand",
    "ro.product.name",
    "ro.build.fingerprint",
    "ro.build.id",
    "ro.build.version.release",
    "ro.build.version.sdk",
    "ro.serialno",
    "ro.build.version.security_patch",
]

for p in props:
    value = run_adb(f"adb -s 192.168.1.19:5555 shell getprop {p}")
    print(f"   {p:35} → {value}")

# ==================== HARDWARE IDs ====================
print("\n🔧 2. HARDWARE IDs")
print(
    f"   Android ID (SSAID)          → {run_adb('adb -s 192.168.1.19:5555 shell settings get secure android_id')}"
)
print(
    f"   Serial Number               → {run_adb('adb -s 192.168.1.19:5555 shell getprop ro.serialno')}"
)

# IMEI (Android 9 cách chuẩn nhất)
imei_raw = run_adb(
    'adb -s 192.168.1.19:5555 shell \'service call iphonesubinfo 1 | cut -d "\\"" -f2 | cut -d " " -f2\''
)
print(
    f"   IMEI                        → {imei_raw if len(imei_raw)>5 else 'Cần root hoặc dùng Xposed'}"
)

# MAC
wifi_mac = run_adb(
    "adb -s 192.168.1.19:5555 shell ip link show wlan0 | grep -o '..:..:..:..:..:..' | head -1"
)
bt_mac = run_adb("adb -s 192.168.1.19:5555 shell settings get secure bluetooth_address")
print(f"   MAC WiFi                    → {wifi_mac}")
print(
    f"   MAC Bluetooth               → {bt_mac if bt_mac != 'Không lấy được' else 'Không đọc được'}"
)

# Google Advertising ID
gaid = run_adb("adb -s 192.168.1.19:5555 shell settings get secure advertising_id")
print(
    f"   Google Advertising ID (GAID)→ {gaid if gaid else 'Chưa có (reset trong Settings)'}"
)

# ==================== THÔNG SỐ KHÁC (dễ bị detect) ====================
print("\n📊 3. THÔNG SỐ KHÁC THƯỜNG BỊ DETECT")
print(
    f"   Màn hình (size)             → {run_adb('adb -s 192.168.1.19:5555 shell wm size')}"
)
print(
    f"   DPI                         → {run_adb('adb -s 192.168.1.19:5555 shell wm density')}"
)
print(
    f"   Timezone                    → {run_adb('adb -s 192.168.1.19:5555 shell getprop persist.sys.timezone')}"
)
print(
    f"   Ngôn ngữ                    → {run_adb('adb -s 192.168.1.19:5555 shell getprop persist.sys.locale')}"
)

# Kernel (rất dễ lộ root)
kernel = run_adb("adb -s 192.168.1.19:5555 shell uname -r")
print(f"   Kernel version              → {kernel}")

print("\n" + "=" * 60)
print("✅ Xong! Copy phần trên paste vào file .txt để so sánh trước/sau spoof nhé.")
print(
    "   Muốn spoof thì dùng MagiskHide Props Config + Tricky Store như tao hướng dẫn trước."
)
