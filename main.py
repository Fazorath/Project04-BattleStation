
import sys



def clear_screen():
    print("\033c", end="")

def print_main_menu():
    print("\n=== BattleStation ===")
    print("Your Modular Terminal Dashboard\n")
    print("1. Project Launcher")
    print("2. Login Logger")
    print("q. Quit")

def get_choice(prompt, valid_choices, default=None):
    choice = input(prompt).strip()
    if not choice and default:
        return default
    while choice not in valid_choices:
        choice = input(f"Invalid choice. {prompt}").strip()
        if not choice and default:
            return default
    return choice

def print_project_menu(projects):
    print("\n=== Project Launcher ===")
    for idx, proj in enumerate(projects, 1):
        print(f"{idx}. {proj}")
    print("q. Quit/Back")


def handle_project_launcher():
    # Example: List projects from a directory and open with VS Code
    import os
    clear_screen()
    projects_dir = "/Users/exempt/Desktop/Projects"
    if not os.path.isdir(projects_dir):
        print(f"Projects directory not found: {projects_dir}")
        return
    projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
    if not projects:
        print("No projects found.")
        return
    print_project_menu(projects)
    valid_choices = [str(i) for i in range(1, len(projects)+1)] + ["q"]
    choice = get_choice(f"Enter project number or q to go back [1-{len(projects)}/q] (q): ", valid_choices, default="q")
    if choice == "q":
        return
    selected = projects[int(choice)-1]
    proj_path = os.path.join(projects_dir, selected)
    print(f"Opening {selected} in VS Code...")
    os.system(f'code "{proj_path}"')

def handle_login_logger():
    from login_logger_menu import login_logger_menu
    login_logger_menu()

def handle_sleep_shortcut():
    print("[Sleep Shortcut] (Not implemented yet)")

def main():
    while True:
        clear_screen()
        print_main_menu()
        choice = get_choice("Select an option [1/2/q] (1): ", ["1", "2", "q"], default="1")
        if choice == "1":
            handle_project_launcher()
        elif choice == "2":
            handle_login_logger()
        elif choice == "q":
            print("Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
