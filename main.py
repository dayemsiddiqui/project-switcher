# project_switcher.py

import yaml
import sys
import os
import subprocess

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'projects.yaml')


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Configuration file not found: {CONFIG_FILE}")
        sys.exit(1)


def execute_command(command):
    subprocess.Popen(command, shell=True)


def start_project(config, project_name):
    project = config['projects'].get(project_name)
    if not project:
        print(f"Project {project_name} not found in configuration.")
        return

    print(f"Starting project: {project_name}")

    # Change to project directory
    project_dir = os.path.expanduser(project['directory'])
    if not os.path.exists(project_dir):
        print(f"Project directory not found: {project_dir}")
        return
    os.chdir(project_dir)

    # Execute startup commands
    for cmd in project.get('startup', []):
        execute_command(cmd)


def stop_project(config, project_name):
    project = config['projects'].get(project_name)
    if not project:
        print(f"Project {project_name} not found in configuration.")
        return

    print(f"Stopping project: {project_name}")

    # Execute shutdown commands
    for cmd in project.get('shutdown', []):
        execute_command(cmd)


def main():
    if len(sys.argv) < 3:
        print("Usage: python project_switcher.py [start|stop|list|fresh_start] [project_name]")
        sys.exit(1)

    action = sys.argv[1]
    project_name = sys.argv[2]

    config = load_config()

    if action == 'start':
        start_project(config, project_name)
    elif action == 'stop':
        stop_project(config, project_name)
    elif action == 'list':
        print("List of projects:")
        for project_name in config['projects']:
            print(f"  - {project_name}")
    elif action == 'fresh_start':
        # Stop all projects
        for name in config['projects']:
            stop_project(config, name)
        # Start the project
        start_project(config, project_name)

    else:
        print(f"Unknown action: {action}")


if __name__ == "__main__":
    main()
