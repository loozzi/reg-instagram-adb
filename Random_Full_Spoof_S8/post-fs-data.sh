#!/system/bin/sh
# Random Full Spoof - post-fs-data.sh
MODDIR=${0%/*}

echo "=== Random Full Spoof đang áp dụng ==="

resetprop ro.build.fingerprint "samsung/beyond1ltexx/beyond1lte:10/QP1A.190711.020/G973FXXU1ATF1:user/release-keys"
resetprop ro.build.description "samsung/beyond1ltexx/beyond1lte:10/QP1A.190711.020/G973FXXU1ATF1:user/release-keys"
resetprop ro.product.model "QP1A.190711.020"
resetprop ro.product.brand "samsung"
resetprop ro.product.name "10"
resetprop ro.product.device "10"
resetprop ro.product.manufacturer "Samsung"
resetprop ro.build.id "TP2A.232321.782"
resetprop ro.build.version.release "10"
resetprop ro.build.version.sdk "31"
resetprop ro.build.version.security_patch "2025-01-15"
resetprop ro.serialno "T79QA7S4LPBCYKLJ"
resetprop ro.boot.serialno "T79QA7S4LPBCYKLJ"
resetprop ro.bootloader "U1S14359"
resetprop ro.build.tags "release-keys"
resetprop ro.build.type "user"

# Hardware IDs
resetprop ro.boot.serialno "T79QA7S4LPBCYKLJ"

# Timezone / Locale
resetprop persist.sys.timezone "America/New_York"
resetprop persist.sys.locale "de-DE"
resetprop ro.product.locale "de-DE"

# Kernel version
resetprop ro.kernel.version "4.9.96-g43b4e3c2a1f8"

# Screen density prop (early boot)
resetprop ro.sf.lcd_density "537"

echo "✅ Random Full Spoof hoàn tất! Android ID = 070ad7aa47bd1c95"
