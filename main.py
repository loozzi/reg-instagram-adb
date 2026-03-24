import random

from lib import PhoneDevice, get_devices


def register_ig(phone: PhoneDevice):
    package_name = phone.get_package_name("./apk/instagram-lite-503-0-0-8-107.apk")

    if not package_name:
        print("Failed to get package name.")
        return

    phone.uninstall_app(package_name)
    phone.install("./apk/instagram-lite-503-0-0-8-107.apk")
    print("Instagram Lite installed successfully.")

    phone.grant_all_permissions(package_name)
    print("Granted all permissions to Instagram Lite.")
    phone.wait(1)

    phone.open(package_name)

    phone.tap(600, 1500)
    phone.wait(1)
    phone.tap(700, 1025)
    phone.wait(1)

    email = "example@example.com"

    phone.input_text(email)
    phone.wait(1)
    phone.tap(700, 760)
    phone.wait(20)
    # TODO: Handle verification code input
    otp = "123456"  # Replace with actual OTP retrieval method
    phone.input_text(otp)
    phone.tap(700, 700)
    phone.wait(5)

    fullname = "John Doe"
    password = "SecurePassword123"

    phone.input_text_unicode(fullname)
    phone.tap(700, 600)
    phone.input_text(password)
    phone.tap(700, 950)
    phone.wait(5)

    for _ in range(random.randint(1, 3)):
        phone.swipe(250, 2500, 250, 2200, 300)
    phone.tap(250, 2500)

    for _ in range(random.randint(1, 3)):
        phone.swipe(720, 2500, 720, 2200, 300)
    phone.tap(720, 2500)

    for _ in range(random.randint(10, 15)):
        phone.swipe(1200, 2500, 1200, 2200, 300)
    phone.tap(1200, 2500)

    phone.tap(700, 2700)
    phone.wait(5)

    phone.tap(700, 2600)

    # TODO: Get cookie here


def __main__():
    devices = get_devices()
    if not devices:
        print("No devices found.")
        return

    phone = devices[0]
    print(f"Using device: {phone}")

    register_ig(phone)
