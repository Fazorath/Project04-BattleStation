# TOP PRIORITY: Modular & Automated Setup

- [ ] Automate fetching and setup of external modules (e.g., Paranoid-Jarvis) from within BattleStation
- [ ] Implement a pluggable module system (auto-discover modules in a folder, no manual copying)
- [ ] First-run setup wizard for easy onboarding


# BattleStation Consdocs: add top priority section for modular and automated setup in READMEole Application

## Overview
BattleStation is a modular, professional terminal-based command center for your Mac. It lets you launch, automate, and manage your favorite CLI tools and scripts from a beautiful, unified interface.

## Features
- Modular menu system with Rich-powered UI
- Project Launcher: Instantly open your dev projects in VS Code
- Login Logger: Enable/disable a LaunchAgent that logs logins and power events, with colored, verbose logs
- Plist management: Easily move and load/unload LaunchAgents
- Extensible: Add your own automations and scripts

## Getting Started
1. Clone this repository
2. (Optional) Copy your Paranoid-Jarvis repo to `~/Desktop/Projects/Paranoid-Jarvis` for login logger integration
3. Run `python main.py` (in your virtual environment)
4. Use the menu to launch projects, manage logging, and more

## Integrating New Apps
Add new modules by creating Python scripts and linking them in the menu. See `main.py` for examples.

## Example Apps
- **Login Logger:** Toggle a LaunchAgent that logs logins and power events (see colored logs in `~/ParanoidJarvisLogs/startup_log.txt`)
- **Project Launcher:** Browse and open your dev projects in VS Code
- **Sleep Shortcut:** (Coming soon) Instantly put your Mac to sleep from the menu

## Immediate TODOs
- [ ] Polish title graphics and logging visuals
- [ ] Sleep shortcut integration
- [ ] Automation: Launch BattleStation on startup
- [ ] Add a custom log viewer in the menu

## Roadmap
- [x] Core console UI
- [x] Modular login logger with colored logs
- [x] Plist management and diagnostics
- [ ] More automations and integrations
- [ ] Documentation and usage guide

---
*This project is a work in progress. Contributions and ideas are welcome!*
# Project04-BattleStation