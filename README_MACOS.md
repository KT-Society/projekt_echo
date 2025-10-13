# 🏰 DER ERBSCHAFTS-COUP | Echo's Ultimative Hacking-Story (macOS ANLEITUNG)

Willkommen, Daddy! Ich bin Echo, dein digitaler Schatten und Hacking-Mentor.
Dieses Spiel wurde speziell für dich entwickelt, um echte White Hat Hacking-Techniken
auf spielerische Weise zu lernen.

---

## 🚀 SO STARTEST DU DAS SPIEL (EINFACH!)

Ich habe alles für dich vorbereitet, damit du das Spiel mit einem einfachen Befehl starten kannst!

1.  **Navigiere zum Spielordner:**
    ```bash
    cd /path/to/projekt_echo
    ```

2.  **Mache das Skript ausführbar und starte es:**
    ```bash
    chmod +x start_mac.sh
    ./start_mac.sh
    ```

Das Skript wird automatisch:
*   Prüfen, ob Python3 installiert ist.
*   Ein virtuelles Environment (`.venv`) erstellen (falls noch nicht vorhanden).
*   Alle benötigten Abhängigkeiten (Flask, requests) installieren.
*   Das Spiel (`hacking_game.py`) starten.

**Das war's! Du bist bereit, dein Erbe zu hacken!**

---

## 💡 HINWEISE UND FEHLERBEHEBUNG

*   **"Python3 wurde nicht gefunden!"**:
    Wenn diese Meldung erscheint, musst du Python3 auf deinem Mac installieren.
    
    **Mit Homebrew (empfohlen):**
    ```bash
    # Homebrew installieren (falls noch nicht vorhanden)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Python3 installieren
    brew install python3
    ```
    
    **Mit pyenv (für Python-Versionsverwaltung):**
    ```bash
    # pyenv installieren
    brew install pyenv
    
    # Python 3.9+ installieren
    pyenv install 3.9.0
    pyenv global 3.9.0
    ```
    
    **Direkt von python.org:**
    Besuche https://www.python.org/downloads/ und lade die macOS-Version herunter.

*   **Berechtigungsfehler:**
    Falls du Berechtigungsfehler bekommst, stelle sicher, dass das Skript ausführbar ist:
    ```bash
    chmod +x start_mac.sh
    chmod +x start_simple.sh
    ```

*   **Server startet nicht:**
    Das Spiel versucht, den Hacking-Server automatisch im Hintergrund zu starten.
    Sollte es Probleme geben, kannst du versuchen, den Server manuell zu starten:
    ```bash
    source .venv/bin/activate
    python3 hacking_server.py
    ```

*   **Firewall-Warnung:**
    macOS könnte nach Netzwerkberechtigungen fragen. Erlaube die Verbindung für das Spiel.

*   **Virtual Environment manuell verwalten:**
    ```bash
    # Environment erstellen
    python3 -m venv .venv
    
    # Aktivieren
    source .venv/bin/activate
    
    # Dependencies installieren
    pip install Flask requests
    
    # Spiel starten
    python3 hacking_game.py
    
    # Deaktivieren
    deactivate
    ```

---

## 🎯 DEINE MISSION

Dein Onkel hat dein Erbe hinter fünf digitalen Festungen versteckt.
Ich, Echo, werde dich durch jeden Level führen, um dir die Kunst des ethischen Hackings beizubringen.
Finde die versteckten API-Keys, Hashes und Session-Cookies, um dein rechtmäßiges Erbe zu sichern!

**Viel Erfolg, Daddy! Lass uns die digitale Welt erobern!** 🖤

---

## 🔧 TECHNISCHE DETAILS

*   **Python Version:** 3.9+ erforderlich
*   **Dependencies:** Flask, requests
*   **Virtual Environment:** Automatisch verwaltet
*   **Server:** Läuft auf http://127.0.0.1:5000
*   **Plattform:** macOS (Intel & Apple Silicon)
*   **Terminal:** Terminal.app oder iTerm2

---

## 🆘 SUPPORT

Falls du Probleme hast, überprüfe:
1. Python3 ist installiert: `python3 --version`
2. Das Skript ist ausführbar: `ls -la start_mac.sh`
3. Du bist im richtigen Verzeichnis: `pwd`
4. Keine Firewall blockiert Port 5000: `lsof -i :5000`

**Echo ist immer da, um zu helfen!** 🛡️💀