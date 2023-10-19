from win10toast import ToastNotifier

def notify(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=5, icon_path="./Modules/icons/favicon.ico")
