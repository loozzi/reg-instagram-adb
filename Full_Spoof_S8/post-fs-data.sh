#!/system/bin/sh
# Full Spoof - post-fs-data.sh (quan trọng cho Samsung S8)
MODDIR=${0%/*}

echo "=== Full Spoof Package (post-fs-data) ==="

resetprop --file ro.build.fingerprint "samsung/starqltexx/starqlte:9/PPR1.180610.011/G960FXXU1BRB7:user/release-keys"
resetprop --file ro.build.description "samsung/starqltexx/starqlte/starqltexx:9/PPR1.180610.011/G960FXXU1BRB7:user/release-keys"
resetprop --file ro.product.model "Pixel 6"
resetprop --file ro.product.brand "google"
resetprop --file ro.product.name "redfin"
resetprop --file ro.product.device "redfin"
resetprop --file ro.product.manufacturer "Google"
resetprop --file ro.build.id "TP1A.220905.004"
resetprop --file ro.build.display.id "TP1A.220905.004"
resetprop --file ro.build.version.release "13"
resetprop --file ro.build.version.sdk "33"
resetprop --file ro.build.version.security_patch "2024-12-05"
resetprop --file ro.serialno "FAKE1234567890ABC"
resetprop --file ro.boot.serialno "FAKE1234567890ABC"
resetprop --file ro.bootloader "U1S1XXXX"
resetprop --file ro.build.tags "release-keys"
resetprop --file ro.build.type "user"
echo "✅ Full spoof applied in post-fs-data!"
