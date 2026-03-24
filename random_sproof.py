import os
import random
import string
import subprocess
import zipfile
from datetime import datetime

print("=" * 90)
print("🔥 MAGISK FULL RANDOM SPOOFER - SAMSUNG S8 ANDROID 9")
print(f"Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("=" * 90)

# ==================== NHẬP ANDROID ID ====================
android_id = (
    input("\nNhập Android ID mới (16 ký tự hex) hoặc Enter để random: ").strip().lower()
)

if not android_id:
    android_id = "".join(random.choices(string.hexdigits.lower(), k=16))
    print(f"→ Random Android ID: {android_id}")
elif len(android_id) != 16 or not all(c in string.hexdigits for c in android_id):
    print("❌ Android ID phải là 16 ký tự hex (0-9, a-f). Script sẽ random thay thế.")
    android_id = "".join(random.choices(string.hexdigits.lower(), k=16))

# ==================== DANH SÁCH FINGERPRINT REAL (2026) ====================
fingerprints = [
    "google/redfin/redfin:13/TP1A.220905.004/1234567:user/release-keys",  # Pixel 6
    "google/barbet/barbet:13/TP1A.220905.004/1234567:user/release-keys",  # Pixel 5a
    "samsung/starqltexx/starqlte:9/PPR1.180610.011/G960FXXU1BRB7:user/release-keys",  # S9
    "samsung/beyond1ltexx/beyond1lte:10/QP1A.190711.020/G973FXXU1ATF1:user/release-keys",  # S10
    "google/coral/coral:12/SP1A.210812.016/1234567:user/release-keys",  # Pixel 4 XL
    "google/bramble/bramble:13/TP1A.220905.004/1234567:user/release-keys",  # Pixel 4a 5G
]

fingerprint = random.choice(fingerprints)

# Tách thông tin
parts = fingerprint.split(":")
brand = parts[0].split("/")[0]
model = parts[1].split("/")[1] if len(parts[1].split("/")) > 1 else "Pixel"
device = parts[1].split("/")[0]
manufacturer = "Google" if "google" in fingerprint else "Samsung"

# Random thêm các thông số
serial = "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
build_id = (
    "TP"
    + str(random.randint(1, 9))
    + "A."
    + str(random.randint(220000, 241231))
    + "."
    + str(random.randint(100, 999))
)
security_patch = (
    f"202{random.randint(4,6)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
)
sdk = random.choice(["28", "29", "30", "31", "33", "34"])
release = "9" if sdk == "28" else random.choice(["10", "11", "12", "13"])

mac_wifi = ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)]).upper()
mac_bt = ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)]).upper()

# Random màn hình / DPI
screen_configs = [
    (1080, 2340, 440),   # Pixel 5a / 4a 5G
    (1080, 2400, 411),   # Pixel 6
    (1440, 3040, 550),   # Galaxy S10
    (1440, 3040, 537),   # Pixel 4 XL
    (1080, 2280, 420),   # Pixel 3a XL
]
screen_w, screen_h, dpi = random.choice(screen_configs)

# Random timezone / locale
timezones = [
    "America/New_York", "America/Los_Angeles", "Europe/London",
    "Europe/Paris", "Asia/Tokyo", "Asia/Singapore", "Asia/Seoul",
]
locales = ["en-US", "en-GB", "ja-JP", "ko-KR", "zh-TW", "fr-FR", "de-DE"]

timezone = random.choice(timezones)
locale = random.choice(locales)

# Random kernel version
kernel_versions = [
    "4.14.117-g4e7e86b6c3e9",
    "4.9.96-g43b4e3c2a1f8",
    "4.19.81-g8c2d1f9b7a45",
    "4.14.180-g1a2b3c4d5e6f",
]
kernel_ver = random.choice(kernel_versions)

print(f"\n✅ Đang tạo profile ngẫu nhiên:")
print(f"   Fingerprint : {fingerprint}")
print(f"   Model       : {model}")
print(f"   Android ID  : {android_id}")
print(f"   Serial      : {serial}")
print(f"   Security Patch: {security_patch}")
print(f"   Màn hình    : {screen_w}x{screen_h}, DPI {dpi}")
print(f"   Timezone    : {timezone}")
print(f"   Locale      : {locale}")
print(f"   Kernel      : {kernel_ver}")

# ==================== TẠO MODULE ====================
module_dir = "Random_Full_Spoof_S8"
os.makedirs(f"{module_dir}/META-INF/com/google/android", exist_ok=True)

# module.prop
with open(f"{module_dir}/module.prop", "w", encoding="utf-8") as f:
    f.write(
        f"""id=random_full_spoof_s8
name=Random Full Spoof S8 ({datetime.now().strftime('%d%m')})
version=1.3
versionCode=4
author=Grok Helper
description=Random spoof full package - Android ID: {android_id}
"""
    )

# post-fs-data.sh (quan trọng nhất cho S8)
post_content = f"""#!/system/bin/sh
# Random Full Spoof - post-fs-data.sh
MODDIR=${{0%/*}}

echo "=== Random Full Spoof đang áp dụng ==="

resetprop ro.build.fingerprint "{fingerprint}"
resetprop ro.build.description "{fingerprint}"
resetprop ro.product.model "{model}"
resetprop ro.product.brand "{brand}"
resetprop ro.product.name "{device}"
resetprop ro.product.device "{device}"
resetprop ro.product.manufacturer "{manufacturer}"
resetprop ro.build.id "{build_id}"
resetprop ro.build.version.release "{release}"
resetprop ro.build.version.sdk "{sdk}"
resetprop ro.build.version.security_patch "{security_patch}"
resetprop ro.serialno "{serial}"
resetprop ro.boot.serialno "{serial}"
resetprop ro.bootloader "U1S1{random.randint(1000,9999)}"
resetprop ro.build.tags "release-keys"
resetprop ro.build.type "user"

# Hardware IDs
resetprop ro.boot.serialno "{serial}"

# Timezone / Locale
resetprop persist.sys.timezone "{timezone}"
resetprop persist.sys.locale "{locale}"
resetprop ro.product.locale "{locale}"

# Kernel version
resetprop ro.kernel.version "{kernel_ver}"

# Screen density prop (early boot)
resetprop ro.sf.lcd_density "{dpi}"

echo "✅ Random Full Spoof hoàn tất! Android ID = {android_id}"
"""

with open(f"{module_dir}/post-fs-data.sh", "w", encoding="utf-8") as f:
    f.write(post_content)

os.chmod(f"{module_dir}/post-fs-data.sh", 0o755)

# service.sh - chạy sau khi boot (cần Android runtime)
service_content = f"""#!/system/bin/sh
# Random Full Spoof - service.sh (chạy sau boot)

# Đợi boot hoàn tất
sleep 5

# Screen size & DPI
wm size {screen_w}x{screen_h}
wm density {dpi}

# Android ID
settings put secure android_id {android_id}

# Timezone
settings put global time_zone "{timezone}"

# Locale / Language
settings put system system_locales "{locale}"

echo "✅ service.sh: screen={screen_w}x{screen_h} dpi={dpi} tz={timezone} locale={locale}"
"""

with open(f"{module_dir}/service.sh", "w", encoding="utf-8") as f:
    f.write(service_content)

os.chmod(f"{module_dir}/service.sh", 0o755)

# Tạo zip
zip_name = "Random_Full_Spoof_S8.zip"
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(module_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, module_dir)
            zipf.write(file_path, arcname)

print(f"\n✅ Module zip đã tạo: {zip_name}")

# Push lên máy
print("\n📤 Đang push module lên điện thoại...")
try:
    subprocess.run(
        f'adb -s 192.168.1.19:5555 push "{zip_name}" /sdcard/Download/{zip_name}',
        shell=True,
        check=True,
    )
    print("✅ Push thành công!")
except Exception as e:
    print(f"❌ Lỗi push: {e}")

print("\n" + "=" * 90)
print("📱 Đang flash module qua ADB...")
try:
    subprocess.run(
        f'adb -s 192.168.1.19:5555 shell "su -c \'magisk --install-module /sdcard/Download/{zip_name}\'"',
        shell=True,
        check=True,
    )
    print("✅ Flash thành công!")
except Exception as e:
    print(f"❌ Lỗi flash: {e}")

print("\n🔄 Đang reboot...")
try:
    subprocess.run(
        "adb -s 192.168.1.19:5555 reboot",
        shell=True,
        check=True,
    )
    print("✅ Reboot lệnh đã gửi!")
except Exception as e:
    print(f"❌ Lỗi reboot: {e}")

print("=" * 90)
print("\nSau reboot, chạy script check để xem kết quả.")
print("Chạy lại script này bất cứ lúc nào để tạo profile NGẪU NHIÊN mới hoàn toàn!")
