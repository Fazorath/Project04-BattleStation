import datetime
import os
import configparser
import subprocess

def get_log_path():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'paranoid_jarvis.conf'))
    output_dir = os.path.expanduser(config.get('general', 'output_dir', fallback='~/ParanoidJarvisLogs'))
    os.makedirs(output_dir, exist_ok=True)
    log_file = config.get('general', 'log_file', fallback='startup_log.txt')
    return os.path.join(output_dir, log_file)

def log_startup_time():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_path = get_log_path()
    # Write with rich color tags for login event
    log_line = f"[green][{now}][/green] [bold cyan]EVENT:[/bold cyan] User login detected on MacBook Pro (exempt)\n"
    with open(log_path, 'a') as f:
        f.write(log_line)

def log_power_status():
    try:
        output = subprocess.check_output(['pmset', '-g', 'batt'], text=True)
        if 'AC Power' in output:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_path = get_log_path()
            # Write with rich color tags for power event
            log_line = f"[yellow][{now}][/yellow] [bold magenta]EVENT:[/bold magenta] Power cable connected\n"
            with open(log_path, 'a') as f:
                f.write(log_line)
    except Exception:
        pass

def main():
    log_startup_time()
    log_power_status()

if __name__ == "__main__":
    main()
