#!/usr/bin/env python3
"""
Shop Street E-commerce Platform Setup Script
This script helps set up the development environment for Shop Street.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n[INFO] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error during {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if required software is installed."""
    print("[INFO] Checking requirements...")
    
    # Check Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("[ERROR] Python 3.8+ is required")
        return False
    print(f"[SUCCESS] Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"[SUCCESS] Node.js {result.stdout.strip()}")
    except FileNotFoundError:
        print("[ERROR] Node.js is required for TailwindCSS")
        return False
    
    return True

def setup_python_environment():
    """Set up Python virtual environment and install dependencies."""
    print("\n[INFO] Setting up Python environment...")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists('venv'):
        if not run_command('python -m venv venv', 'Creating virtual environment'):
            return False
    
    # Determine activation script based on OS
    if platform.system() == 'Windows':
        activate_script = 'venv\\Scripts\\activate'
        pip_command = 'venv\\Scripts\\pip'
        python_command = 'venv\\Scripts\\python'
    else:
        activate_script = 'source venv/bin/activate'
        pip_command = 'venv/bin/pip'
        python_command = 'venv/bin/python'
    
    # Install Python dependencies
    if not run_command(f'{pip_command} install -r requirements.txt', 'Installing Python dependencies'):
        return False
    
    return True, python_command

def setup_node_environment():
    """Set up Node.js environment and install dependencies."""
    print("\n[INFO] Setting up Node.js environment...")
    
    if not run_command('npm install', 'Installing Node.js dependencies'):
        return False
    
    if not run_command('npm run build-css', 'Building TailwindCSS'):
        return False
    
    return True

def setup_django():
    """Set up Django project."""
    print("\n[INFO] Setting up Django project...")
    
    # Determine Python command
    if platform.system() == 'Windows':
        python_command = 'venv\\Scripts\\python'
    else:
        python_command = 'venv/bin/python'
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            if platform.system() == 'Windows':
                run_command('copy .env.example .env', 'Creating .env file')
            else:
                run_command('cp .env.example .env', 'Creating .env file')
            print("[INFO] Please edit .env file with your configuration")
    
    # Run migrations
    if not run_command(f'{python_command} manage.py makemigrations', 'Creating migrations'):
        return False
    
    if not run_command(f'{python_command} manage.py migrate', 'Running migrations'):
        return False
    
    # Create superuser (optional)
    print("\n[INFO] Create a superuser account for admin access:")
    print("Run: python manage.py createsuperuser")
    
    return True

def main():
    """Main setup function."""
    print("Welcome to Shop Street E-commerce Platform Setup!")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n[ERROR] Setup failed: Missing requirements")
        sys.exit(1)
    
    # Setup Python environment
    result = setup_python_environment()
    if not result:
        print("\n[ERROR] Setup failed: Python environment setup failed")
        sys.exit(1)
    
    # Setup Node.js environment
    if not setup_node_environment():
        print("\n[ERROR] Setup failed: Node.js environment setup failed")
        sys.exit(1)
    
    # Setup Django
    if not setup_django():
        print("\n[ERROR] Setup failed: Django setup failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("[SUCCESS] Shop Street setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the development server: python manage.py runserver")
    print("4. Visit http://127.0.0.1:8000 to see your e-commerce platform!")
    print("\nFor more information, check README.md")

if __name__ == '__main__':
    main()