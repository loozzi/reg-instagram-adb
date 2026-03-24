import os
import subprocess
import zipfile
from datetime import datetime

print("=" * 85)
print("🔥 TẠO MAGISK MODULE SPOOF FULL PACKAGE - SAMSUNG S8 (Android 9)")
print(f"Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("=" * 85)

# ==================== NHẬP FINGERPRINT ====================
print(
    "\n📋 Dán fingerprint mới (hoặc Enter để dùng mẫu Pixel 6 - khuyến nghị cho test):"
)
print("   Ví dụ: google/redfin/redfin:13/TP1A.220905.004/1234567:user/release-keys")
fp_input = input("> ").strip()

if fp_input:
    fingerprint = fp_input
else:
    # Mẫu tốt cho S8 Android 9 (ít xung đột)
    fingerprint = "google/redfin/redfin:13/TP1A.220905.004/1234567:user/release-keys"
    print(f"   → Dùng mặc định: {fingerprint}")

# Tách thông tin từ fingerprint
try:
    build_desc = (
        fingerprint.split(":")[0]
        + "/"
        + fingerprint.split("/")[1]
        + ":"
        + ":".join(fingerprint.split(":")[1:])
    )
except:
    build_desc = fingerprint

# ==================== CẤU HÌNH FULL PROP (15 prop quan trọng) ====================
print("\n🔧 Đang tạo full spoof package (15 props)...")

props = {
    "ro.build.fingerprint": fingerprint,
    "ro.build.description": build_desc,
    "ro.product.model": "Pixel 6",  # thay đổi nếu muốn
    "ro.product.brand": "google",
    "ro.product.name": "redfin",
    "ro.product.device": "redfin",
    "ro.product.manufacturer": "Google",
    "ro.build.id": "TP1A.220905.004",
    "ro.build.display.id": "TP1A.220905.004",
    "ro.build.version.release": "13",
    "ro.build.version.sdk": "33",
    "ro.build.version.security_patch": "2024-12-05",  # fake ngày mới
    "ro.serialno": "FAKE1234567890ABC",
    "ro.boot.serialno": "FAKE1234567890ABC",
    "ro.bootloader": "U1S1XXXX",
    "ro.build.tags": "release-keys",
    "ro.build.type": "user",
}

# Tạo thư mục module
module_dir = "Full_Spoof_S8"
os.makedirs(f"{module_dir}/system", exist_ok=True)
os.makedirs(f"{module_dir}/META-INF/com/google/android", exist_ok=True)

# module.prop
with open(f"{module_dir}/module.prop", "w", encoding="utf-8") as f:
    f.write(
        f"""id=full_spoof_s8
name=Full Spoof Package S8 (15 props)
version=1.2
versionCode=3
author=Script by Grok
description=Spoof fingerprint + 15 prop quan trọng cho test hệ thống - {datetime.now().strftime('%d/%m/%Y')}
"""
    )

# customize.sh (áp dụng tất cả prop)
customize_content = """#!/system/bin/sh
# Full Spoof Package - customize.sh
MODDIR=${0%/*}

echo "=== Full Spoof Package đang áp dụng 15 props ==="

"""
for key, value in props.items():
    customize_content += f'resetprop {key} "{value}"\n'

customize_content += """
echo "✅ Full spoof hoàn tất! Reboot để áp dụng."
"""

with open(f"{module_dir}/customize.sh", "w", encoding="utf-8") as f:
    f.write(customize_content)

os.chmod(f"{module_dir}/customize.sh", 0o755)

# Tạo zip
zip_name = "Full_Spoof_S8.zip"
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(module_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, module_dir)
            zipf.write(file_path, arcname)

print(f"\n✅ Module zip đã tạo: {zip_name}")

# Push lên điện thoại qua ADB
print("\n📤 Đang push module lên /sdcard/Download/ ...")
try:
    subprocess.run(
        f'adb push "{zip_name}" /sdcard/Download/{zip_name}', shell=True, check=True
    )
    print("✅ Push thành công!")
except Exception as e:
    print(f"❌ Lỗi push: {e}")
    print("Kiểm tra ADB kết nối (adb devices)")

print("\n" + "=" * 85)
print("📱 CÁCH FLASH MODULE (chọn 1 trong 2):")
print("Cách A - Nhanh nhất (dùng ADB + root):")
print(f"   adb shell \"su -c 'magisk --install-module /sdcard/Download/{zip_name}'\"")
print("   Sau đó reboot máy.")
print("\nCách B - An toàn (qua giao diện):")
print("   1. Mở Magisk Manager trên S8")
print("   2. Modules → Install from storage")
print(f"   3. Chọn file {zip_name} trong thư mục Download")
print("   4. Install → Reboot")
print("=" * 85)

print("\nSau khi reboot, chạy script check_device trước đó để verify.")
print(
    "Muốn chỉnh model/brand/security_patch khác hoặc thêm spoof MAC/IMEI thì báo tao nhé!"
)
