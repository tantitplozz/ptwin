#!/usr/bin/env python3
"""
🔥 GOD-TIER PhantomAutoBuyBot - Quick Start Runner
Easy deployment and testing script
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path

def print_banner():
    """Print GOD-TIER banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🔥 GOD-TIER PhantomAutoBuyBot FULL STACK 🔥          ║
    ║                                                              ║
    ║  🧠 Advanced Memory System    📊 Real-time Monitoring       ║
    ║  🛡️ Maximum Stealth Tech     📱 Telegram Notifications     ║
    ║  🔥 Warmup Agent             🧪 A/B Testing Engine          ║
    ║  💳 Smart Payment System     🤖 Dynamic Agent Behavior     ║
    ║  🔐 OTP Automation           🐳 Docker Ready               ║
    ║                                                              ║
    ║              Ready for iPhone 16 Pro Max Mission!           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 [SETUP] Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ [ERROR] Python 3.10+ required")
        return False
        
    # Check .env file
    if not Path(".env").exists():
        print("⚠️ [WARNING] .env file not found")
        print("📝 [INFO] Copying .env.template to .env")
        subprocess.run(["cp", ".env.template", ".env"])
        print("✏️ [ACTION] Please edit .env file with your credentials")
        return False
        
    # Check Docker
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print("✅ [SETUP] Docker available")
    except:
        print("⚠️ [WARNING] Docker not available - will run in local mode")
        
    print("✅ [SETUP] Requirements check completed")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 [SETUP] Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ [SETUP] Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ [ERROR] Failed to install dependencies")
        return False

def run_local():
    """Run bot locally"""
    print("🚀 [LOCAL] Starting GOD-TIER PhantomAutoBuyBot locally...")
    
    try:
        # Change to phantom_autobuy directory and run main.py
        os.chdir("phantom_autobuy")
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n⚠️ [LOCAL] Bot stopped by user")
    except Exception as e:
        print(f"❌ [LOCAL] Error: {e}")

def run_docker():
    """Run bot with Docker"""
    print("🐳 [DOCKER] Starting GOD-TIER PhantomAutoBuyBot with Docker...")
    
    try:
        # Build and run with docker-compose
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except KeyboardInterrupt:
        print("\n⚠️ [DOCKER] Stopping containers...")
        subprocess.run(["docker-compose", "down"])
    except subprocess.CalledProcessError:
        print("❌ [DOCKER] Failed to start with Docker")

def show_menu():
    """Show main menu"""
    print("\n🎯 [MENU] Choose deployment option:")
    print("1. 🚀 Run Locally (Python)")
    print("2. 🐳 Run with Docker")
    print("3. 📊 Monitor Only (WebSocket Dashboard)")
    print("4. 🧪 Test Configuration")
    print("5. 📝 Edit Configuration")
    print("6. 🔧 Install Dependencies")
    print("7. ❌ Exit")
    
    choice = input("\n👉 Enter your choice (1-7): ").strip()
    return choice

def test_configuration():
    """Test bot configuration"""
    print("🧪 [TEST] Testing configuration...")
    
    # Test imports
    try:
        sys.path.append("phantom_autobuy")
        import config
        print("✅ [TEST] Configuration loaded successfully")
        
        # Test required variables
        required_vars = ["GOLOGIN_API_KEY", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"]
        missing_vars = []
        
        for var in required_vars:
            if not getattr(config, var, None):
                missing_vars.append(var)
                
        if missing_vars:
            print(f"⚠️ [TEST] Missing required variables: {', '.join(missing_vars)}")
            print("📝 [TEST] Please update your .env file")
        else:
            print("✅ [TEST] All required variables configured")
            
    except ImportError as e:
        print(f"❌ [TEST] Import error: {e}")
        print("📦 [TEST] Try installing dependencies first")

def edit_configuration():
    """Edit configuration file"""
    print("📝 [CONFIG] Opening .env file for editing...")
    
    editors = ["nano", "vim", "vi", "code", "notepad"]
    
    for editor in editors:
        try:
            subprocess.run([editor, ".env"], check=True)
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    else:
        print("⚠️ [CONFIG] No suitable editor found")
        print("📝 [CONFIG] Please edit .env file manually")

def monitor_only():
    """Run monitor dashboard only"""
    print("📊 [MONITOR] Starting WebSocket monitor...")
    
    try:
        sys.path.append("phantom_autobuy")
        from monitor_ws import start_monitor
        asyncio.run(start_monitor())
    except KeyboardInterrupt:
        print("\n⚠️ [MONITOR] Monitor stopped")
    except Exception as e:
        print(f"❌ [MONITOR] Error: {e}")

def main():
    """Main function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ [SETUP] Please fix the issues above and try again")
        return
        
    while True:
        choice = show_menu()
        
        if choice == "1":
            run_local()
        elif choice == "2":
            run_docker()
        elif choice == "3":
            monitor_only()
        elif choice == "4":
            test_configuration()
        elif choice == "5":
            edit_configuration()
        elif choice == "6":
            install_dependencies()
        elif choice == "7":
            print("👋 [EXIT] Goodbye! May your iPhone purchases be swift and successful!")
            break
        else:
            print("❌ [ERROR] Invalid choice. Please try again.")
            
        input("\n⏸️ Press Enter to continue...")

if __name__ == "__main__":
    main()