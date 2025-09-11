
import sys


def render_menu():
    print("\n=== BattleStation ===")
    print("Your Modular Terminal Dashboard\n")
    print("1. Project Launcher")
    print("2. Login Logger")
    print("q. Quit")


def handle_project_launcher():
    # Example: List projects from a directory and open with VS Code
    import os
    print("\033c", end="")  # Clear screen
    projects_dir = "/Users/exempt/Desktop/Projects"
    if not os.path.isdir(projects_dir):
        print(f"Projects directory not found: {projects_dir}")
        return
    projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
    if not projects:
        print("No projects found.")
        return
    print("\n=== Project Launcher ===")
    for idx, proj in enumerate(projects, 1):
        print(f"{idx}. {proj}")
    print("q. Quit/Back")
    valid_choices = [str(i) for i in range(1, len(projects)+1)] + ["q"]
    choice = input(f"Enter project number or q to go back [1-{len(projects)}/q] (q): ").strip()
    if choice == "q" or choice not in valid_choices:
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
        print("\033c", end="")  # Clear screen
        render_menu()
        choice = input("Select an option [1/2/q] (1): ").strip() or "1"
        if choice == "1":
            handle_project_launcher()
        elif choice == "2":
            handle_login_logger()
        elif choice == "q":
            print("Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
