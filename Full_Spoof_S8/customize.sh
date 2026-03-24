#!/system/bin/sh
# Full Spoof Package - customize.sh
MODDIR=${0%/*}

echo "=== Full Spoof Package đang áp dụng 15 props ==="

resetprop ro.build.fingerprint "samsung/starqltexx/starqlte:9/PPR1.180610.011/G960FXXU1BRB7:user/release-keys"
resetprop ro.build.description "samsung/starqltexx/starqlte/starqltexx:9/PPR1.180610.011/G960FXXU1BRB7:user/release-keys"
resetprop ro.product.model "Pixel 6"
resetprop ro.product.brand "google"
resetprop ro.product.name "redfin"
resetprop ro.product.device "redfin"
resetprop ro.product.manufacturer "Google"
resetprop ro.build.id "TP1A.220905.004"
resetprop ro.build.display.id "TP1A.220905.004"
resetprop ro.build.version.release "13"
resetprop ro.build.version.sdk "33"
resetprop ro.build.version.security_patch "2024-12-05"
resetprop ro.serialno "FAKE1234567890ABC"
resetprop ro.boot.serialno "FAKE1234567890ABC"
resetprop ro.bootloader "U1S1XXXX"
resetprop ro.build.tags "release-keys"
resetprop ro.build.type "user"

echo "✅ Full spoof hoàn tất! Reboot để áp dụng."
