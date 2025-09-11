import os
import webbrowser
from quick_launch_apps.apps import APPS
from quick_launch_websites.websites import WEBSITES

def clear_screen():
    print("\033c", end="")


def print_quick_launch_menu():
    print("=== Quick Launch ===\n")
    print("1. Launch App")
    print("2. Open Website")
    print("q. Quit/Back")

def print_apps_menu():
    print("\n--- Apps ---")
    for idx, app in enumerate(APPS, 1):
        print(f"{idx}. {app['name']}")
    print("q. Quit/Back")

def print_websites_menu():
    print("\n--- Websites ---")
    for idx, site in enumerate(WEBSITES, 1):
        print(f"{idx}. {site['name']}")
    print("q. Quit/Back")

def quick_launch_menu():
    while True:
        clear_screen()
        print_quick_launch_menu()
        choice = input("Select an option [1/2/q] (q): ").strip() or "q"
        if choice == "1":
            while True:
                clear_screen()
                print_apps_menu()
                app_choices = [str(i) for i in range(1, len(APPS)+1)] + ["q"]
                app_choice = input(f"Select app [1-{len(APPS)}/q] (q): ").strip() or "q"
                if app_choice == "q":
                    break
                idx = int(app_choice) - 1
                app = APPS[idx]
                clear_screen()
                print(f"Launching {app['name']}...")
                os.system(app["command"])
                input("\nPress Enter to return to the Apps menu...")
        elif choice == "2":
            while True:
                clear_screen()
                print_websites_menu()
                web_choices = [str(i) for i in range(1, len(WEBSITES)+1)] + ["q"]
                web_choice = input(f"Select website [1-{len(WEBSITES)}/q] (q): ").strip() or "q"
                if web_choice == "q":
                    break
                idx = int(web_choice) - 1
                site = WEBSITES[idx]
                clear_screen()
                print(f"Opening {site['url']} in browser...")
                webbrowser.open(site["url"])
                input("\nPress Enter to return to the Websites menu...")
        elif choice == "q":
            break
