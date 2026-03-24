#!/system/bin/sh
# Random Full Spoof - service.sh (chạy sau boot)

# Đợi boot hoàn tất
sleep 5

# Screen size & DPI
wm size 1440x3040
wm density 537

# Android ID
settings put secure android_id 070ad7aa47bd1c95

# Timezone
settings put global time_zone "America/New_York"

# Locale / Language
settings put system system_locales "de-DE"

echo "✅ service.sh: screen=1440x3040 dpi=537 tz=America/New_York locale=de-DE"
