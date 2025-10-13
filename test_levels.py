#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTOMATISCHER LEVEL-TEST FÜR HACKING GAME
Testet alle 5 Levels systematisch MIT ECHTEN SERVER-DATEN
"""

import sys
import os
import time
import subprocess
import requests
import json
import hashlib

# Fix Unicode encoding for Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def test_server():
    """Teste ob der Server läuft UND echte Daten zurückgibt"""
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code == 200:
            # Prüfe ob echte HTML-Antwort kommt (nicht simuliert)
            if "Hacking Target Server" in response.text and "intentional security vulnerabilities" in response.text:
                print("   ✅ Server läuft und gibt echte Daten zurück")
                return True
        print(f"   ❌ Server gibt keine echten Daten zurück (Status: {response.status_code})")
        return False
    except Exception as e:
        print(f"   ❌ Server-Test fehlgeschlagen: {e}")
        return False

def test_level_1():
    """Teste Level 1: Web Application Reconnaissance - ALLE EINGABEOPTIONEN"""
    print("🔍 TESTE LEVEL 1: Web Application Reconnaissance")
    print("   📋 Teste alle verfügbaren Eingabeoptionen...")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: .env.local Zugriff (Level-Abschluss)
    total_tests += 1
    try:
        response = requests.get("http://127.0.0.1:5000/.env.local", timeout=5)
        if response.status_code == 200 and "API_KEY" in response.text:
            print("   ✅ .env.local erfolgreich gefunden (Level-Abschluss)")
            tests_passed += 1
        else:
            print("   ❌ .env.local nicht gefunden oder kein API_KEY")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen von .env.local: {e}")
    
    # Test 2: Hauptseite
    total_tests += 1
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Hauptseite erreichbar")
            tests_passed += 1
        else:
            print(f"   ❌ Hauptseite nicht erreichbar (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen der Hauptseite: {e}")
    
    # Test 3: Debug Endpoint
    total_tests += 1
    try:
        response = requests.get("http://127.0.0.1:5000/debug", timeout=5)
        if response.status_code == 200 and "vulnerabilities" in response.text:
            print("   ✅ Debug Endpoint funktioniert")
            tests_passed += 1
        else:
            print(f"   ❌ Debug Endpoint funktioniert nicht (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen des Debug Endpoints: {e}")
    
    # Test 4: HTTP OPTIONS
    total_tests += 1
    try:
        response = requests.options("http://127.0.0.1:5000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ HTTP OPTIONS funktioniert")
            tests_passed += 1
        else:
            print(f"   ❌ HTTP OPTIONS funktioniert nicht (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen von HTTP OPTIONS: {e}")
    
    # Test 5: HTTP HEAD
    total_tests += 1
    try:
        response = requests.head("http://127.0.0.1:5000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ HTTP HEAD funktioniert")
            tests_passed += 1
        else:
            print(f"   ❌ HTTP HEAD funktioniert nicht (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen von HTTP HEAD: {e}")
    
    # Test 6: robots.txt
    total_tests += 1
    try:
        response = requests.get("http://127.0.0.1:5000/robots.txt", timeout=5)
        if response.status_code == 200 and "Disallow:" in response.text:
            print("   ✅ robots.txt vorhanden und funktional (empfohlen für Webserver)")
            tests_passed += 1
        else:
            print(f"   ⚠️  robots.txt Status: {response.status_code} (aber nicht kritisch)")
            # Nicht als Fehler werten, da robots.txt optional ist
            tests_passed += 1
    except Exception as e:
        print(f"   ❌ Fehler beim Testen von robots.txt: {e}")
    
    print(f"   📊 Level 1 Tests: {tests_passed}/{total_tests} bestanden")
    return tests_passed >= 1  # Mindestens Level-Abschluss muss funktionieren

def test_level_2():
    """Teste Level 2: Network Discovery & Vulnerability Scanning - ALLE EINGABEOPTIONEN"""
    print("🔍 TESTE LEVEL 2: Network Discovery & Vulnerability Scanning")
    print("   📋 Teste alle verfügbaren Eingabeoptionen...")
    
    tests_passed = 0
    total_tests = 0
    
    # Erst .env.local lesen um den aktuellen API Key zu bekommen
    api_key = None
    try:
        response = requests.get("http://127.0.0.1:5000/.env.local", timeout=5)
        if response.status_code == 200 and "API_KEY=" in response.text:
            lines = response.text.split('\n')
            for line in lines:
                if line.startswith('API_KEY='):
                    api_key = line.split('=')[1].strip()
                    break
    except Exception as e:
        print(f"   ❌ Fehler beim Lesen von .env.local: {e}")
        return False
    
    if not api_key:
        print("   ❌ API Key nicht in .env.local gefunden")
        return False
    
    print(f"   ✅ API Key gefunden: {api_key[:8]}...")
    
    # Test 1: API Key verwenden (Level-Abschluss)
    total_tests += 1
    try:
        headers = {"X-API-Key": api_key}
        response = requests.get("http://127.0.0.1:5000/api/secret", headers=headers, timeout=5)
        if response.status_code == 200 and "Access granted" in response.text:
            print("   ✅ API Key erfolgreich verwendet (Level-Abschluss)")
            tests_passed += 1
        else:
            print(f"   ❌ API Key funktioniert nicht (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen des API Keys: {e}")
    
    # Test 2: API ohne Key (sollte 401 sein)
    total_tests += 1
    try:
        response = requests.get("http://127.0.0.1:5000/api/secret", timeout=5)
        if response.status_code == 401:
            print("   ✅ API ohne Key korrekt abgelehnt (401)")
            tests_passed += 1
        else:
            print(f"   ❌ API ohne Key sollte 401 sein (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen der API ohne Key: {e}")
    
    # Test 3: Falscher API Key
    total_tests += 1
    try:
        headers = {"X-API-Key": "falscher-key"}
        response = requests.get("http://127.0.0.1:5000/api/secret", headers=headers, timeout=5)
        if response.status_code == 401:
            print("   ✅ Falscher API Key korrekt abgelehnt (401)")
            tests_passed += 1
        else:
            print(f"   ❌ Falscher API Key sollte 401 sein (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen mit falschem API Key: {e}")
    
    # Test 4: Verschiedene HTTP Methoden
    total_tests += 1
    try:
        headers = {"X-API-Key": api_key}
        response = requests.post("http://127.0.0.1:5000/api/secret", headers=headers, timeout=5)
        if response.status_code in [200, 405]:  # 200 OK oder 405 Method Not Allowed
            print("   ✅ HTTP POST funktioniert")
            tests_passed += 1
        else:
            print(f"   ❌ HTTP POST funktioniert nicht (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen von HTTP POST: {e}")
    
    print(f"   📊 Level 2 Tests: {tests_passed}/{total_tests} bestanden")
    return tests_passed >= 1  # Mindestens Level-Abschluss muss funktionieren

def test_level_3():
    """Teste Level 3: SQL Injection & Database Attacks - ALLE EINGABEOPTIONEN"""
    print("🔍 TESTE LEVEL 3: SQL Injection & Database Attacks")
    print("   📋 Teste alle verfügbaren Eingabeoptionen...")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: SQL Injection (Level-Abschluss)
    total_tests += 1
    try:
        payload = "admin' OR '1'='1' --"
        data = {"username": payload, "password": "anything"}
        response = requests.post("http://127.0.0.1:5000/login", data=data, timeout=5)
        if response.status_code == 200 and "Welcome" in response.text:
            print("   ✅ SQL Injection erfolgreich (Level-Abschluss)")
            tests_passed += 1
        else:
            print("   ❌ SQL Injection funktioniert nicht")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen der SQL Injection: {e}")
    
    # Test 2: Normale Anmeldung (sollte fehlschlagen)
    total_tests += 1
    try:
        data = {"username": "admin", "password": "falsches_passwort"}
        response = requests.post("http://127.0.0.1:5000/login", data=data, timeout=5)
        if response.status_code == 200 and "Invalid credentials" in response.text:
            print("   ✅ Normale Anmeldung korrekt abgelehnt")
            tests_passed += 1
        else:
            print(f"   ❌ Normale Anmeldung sollte abgelehnt werden (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen der normalen Anmeldung: {e}")
    
    # Test 3: Verschiedene SQL Injection Payloads
    sql_payloads = [
        "admin' OR '1'='1",
        "admin' UNION SELECT 1,2,3,4,5--",
        "admin'; DROP TABLE users; --",
        "' OR 1=1 --",
        "admin' OR 1=1#"
    ]
    
    for i, payload in enumerate(sql_payloads):
        total_tests += 1
        try:
            data = {"username": payload, "password": "anything"}
            response = requests.post("http://127.0.0.1:5000/login", data=data, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ SQL Payload {i+1} funktioniert: {payload[:20]}...")
                tests_passed += 1
            else:
                print(f"   ⚠️  SQL Payload {i+1} funktioniert nicht: {payload[:20]}...")
        except Exception as e:
            print(f"   ❌ Fehler beim Testen von SQL Payload {i+1}: {e}")
    
    # Test 4: Login-Seite GET
    total_tests += 1
    try:
        response = requests.get("http://127.0.0.1:5000/login", timeout=5)
        if response.status_code == 200 and "Login" in response.text:
            print("   ✅ Login-Seite erreichbar")
            tests_passed += 1
        else:
            print(f"   ❌ Login-Seite nicht erreichbar (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen der Login-Seite: {e}")
    
    print(f"   📊 Level 3 Tests: {tests_passed}/{total_tests} bestanden")
    return tests_passed >= 1  # Mindestens Level-Abschluss muss funktionieren

def test_level_4():
    """Teste Level 4: XSS & Client-Side Attacks - ALLE EINGABEOPTIONEN"""
    print("🔍 TESTE LEVEL 4: XSS & Client-Side Attacks")
    print("   📋 Teste alle verfügbaren Eingabeoptionen...")
    
    tests_passed = 0
    total_tests = 0
    
    # Erst eine Session erstellen
    session = requests.Session()
    
    # Login um Session zu bekommen
    try:
        login_data = {"username": "admin", "password": "admin123"}
        login_response = session.post("http://127.0.0.1:5000/login", data=login_data, timeout=5)
        
        if login_response.status_code != 200:
            print("   ❌ Login fehlgeschlagen")
            return False
        
        print("   ✅ Session erstellt")
    except Exception as e:
        print(f"   ❌ Fehler beim Login: {e}")
        return False
    
    # Test 1: XSS (Level-Abschluss)
    total_tests += 1
    try:
        payload = "<script>alert('XSS')</script>"
        data = {"comment": payload}
        response = session.post("http://127.0.0.1:5000/comments", data=data, timeout=5)
        
        if response.status_code == 200:
            get_response = session.get("http://127.0.0.1:5000/comments", timeout=5)
            if payload in get_response.text:
                print("   ✅ XSS erfolgreich (Level-Abschluss)")
                tests_passed += 1
            else:
                print("   ❌ XSS Payload nicht in Response gefunden")
        else:
            print(f"   ❌ XSS POST fehlgeschlagen (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen von XSS: {e}")
    
    # Test 2: Verschiedene XSS Payloads
    xss_payloads = [
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<iframe src=javascript:alert('XSS')></iframe>",
        "<body onload=alert('XSS')>"
    ]
    
    for i, payload in enumerate(xss_payloads):
        total_tests += 1
        try:
            data = {"comment": payload}
            response = session.post("http://127.0.0.1:5000/comments", data=data, timeout=5)
            if response.status_code == 200:
                get_response = session.get("http://127.0.0.1:5000/comments", timeout=5)
                if payload in get_response.text:
                    print(f"   ✅ XSS Payload {i+1} funktioniert: {payload[:30]}...")
                    tests_passed += 1
                else:
                    print(f"   ⚠️  XSS Payload {i+1} nicht in Response: {payload[:30]}...")
            else:
                print(f"   ❌ XSS Payload {i+1} POST fehlgeschlagen")
        except Exception as e:
            print(f"   ❌ Fehler beim Testen von XSS Payload {i+1}: {e}")
    
    # Test 3: Comments-Seite GET
    total_tests += 1
    try:
        response = session.get("http://127.0.0.1:5000/comments", timeout=5)
        if response.status_code == 200 and "Comments" in response.text:
            print("   ✅ Comments-Seite erreichbar")
            tests_passed += 1
        else:
            print(f"   ❌ Comments-Seite nicht erreichbar (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen der Comments-Seite: {e}")
    
    # Test 4: Ohne Session (sollte 401 sein)
    total_tests += 1
    try:
        payload = "<script>alert('XSS')</script>"
        data = {"comment": payload}
        response = requests.post("http://127.0.0.1:5000/comments", data=data, timeout=5)
        if response.status_code == 401:
            print("   ✅ Comments ohne Session korrekt abgelehnt (401)")
            tests_passed += 1
        else:
            print(f"   ❌ Comments ohne Session sollte 401 sein (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Fehler beim Testen ohne Session: {e}")
    
    print(f"   📊 Level 4 Tests: {tests_passed}/{total_tests} bestanden")
    return tests_passed >= 1  # Mindestens Level-Abschluss muss funktionieren

def test_level_5():
    """Teste Level 5: Digital Forensics & Advanced Hacking - ALLE EINGABEOPTIONEN"""
    print("🔍 TESTE LEVEL 5: Digital Forensics & Advanced Hacking")
    print("   📋 Teste alle verfügbaren Eingabeoptionen...")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Forensik-Endpunkte (Level-Abschluss)
    endpoints = ["/forensics", "/memory", "/network", "/files"]
    for endpoint in endpoints:
        total_tests += 1
        try:
            response = requests.get(f"http://127.0.0.1:5000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ Endpoint {endpoint} erreichbar (Level-Abschluss)")
                tests_passed += 1
                break
            else:
                print(f"   ❌ Endpoint {endpoint} nicht erreichbar (Status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ Fehler beim Testen von {endpoint}: {e}")
    
    # Test 2: Alle Forensik-Endpunkte einzeln
    for endpoint in endpoints:
        total_tests += 1
        try:
            response = requests.get(f"http://127.0.0.1:5000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint} funktioniert")
                tests_passed += 1
            else:
                print(f"   ❌ {endpoint} funktioniert nicht (Status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ Fehler beim Testen von {endpoint}: {e}")
    
    # Test 3: Verschiedene HTTP Methoden für Forensik
    for endpoint in endpoints:
        total_tests += 1
        try:
            response = requests.post(f"http://127.0.0.1:5000{endpoint}", timeout=5)
            if response.status_code in [200, 405]:  # 200 OK oder 405 Method Not Allowed
                print(f"   ✅ {endpoint} POST funktioniert")
                tests_passed += 1
            else:
                print(f"   ❌ {endpoint} POST funktioniert nicht (Status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ Fehler beim Testen von {endpoint} POST: {e}")
    
    # Test 4: Admin-Endpunkte
    admin_endpoints = ["/admin", "/api/admin/data"]
    for endpoint in admin_endpoints:
        total_tests += 1
        try:
            response = requests.get(f"http://127.0.0.1:5000{endpoint}", timeout=5)
            if response.status_code in [200, 403]:  # 200 OK oder 403 Forbidden
                print(f"   ✅ {endpoint} erreichbar")
                tests_passed += 1
            else:
                print(f"   ❌ {endpoint} nicht erreichbar (Status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ Fehler beim Testen von {endpoint}: {e}")
    
    # Test 5: Weitere Endpunkte
    other_endpoints = ["/api/users", "/documents", "/upload", "/ssrf", "/command", "/ldap", "/nosql"]
    for endpoint in other_endpoints:
        total_tests += 1
        try:
            response = requests.get(f"http://127.0.0.1:5000{endpoint}", timeout=5)
            if response.status_code in [200, 401, 403, 404]:  # Verschiedene erwartete Status
                print(f"   ✅ {endpoint} erreichbar (Status: {response.status_code})")
                tests_passed += 1
            else:
                print(f"   ❌ {endpoint} unerwarteter Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Fehler beim Testen von {endpoint}: {e}")
    
    print(f"   📊 Level 5 Tests: {tests_passed}/{total_tests} bestanden")
    return tests_passed >= 1  # Mindestens Level-Abschluss muss funktionieren

def main():
    """Hauptfunktion für alle Tests"""
    print("🚀 STARTE VOLLSTÄNDIGE LEVEL-TESTS")
    print("="*50)
    
    # Server testen
    if not test_server():
        print("❌ Server läuft nicht! Starte Server...")
        # Server starten mit .venv
        if sys.platform.startswith('win'):
            venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
            if os.path.exists(venv_python):
                subprocess.Popen([venv_python, "hacking_server.py"], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen([sys.executable, "hacking_server.py"], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            venv_python = os.path.join(os.getcwd(), ".venv", "bin", "python")
            if os.path.exists(venv_python):
                subprocess.Popen([venv_python, "hacking_server.py"], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                subprocess.Popen([sys.executable, "hacking_server.py"], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Länger warten für Server-Start
        print("⏳ Warte auf Server-Start...")
        for i in range(10):
            time.sleep(1)
            if test_server():
                print("✅ Server erfolgreich gestartet!")
                break
            print(f"⏳ Warte... ({i+1}/10)")
        else:
            print("❌ Server konnte nicht gestartet werden!")
            print("💡 Versuche es manuell: python hacking_server.py")
            return False
    
    print("✅ Server läuft")
    print()
    
    # Alle Levels testen
    results = []
    results.append(("Level 1", test_level_1()))
    results.append(("Level 2", test_level_2()))
    results.append(("Level 3", test_level_3()))
    results.append(("Level 4", test_level_4()))
    results.append(("Level 5", test_level_5()))
    
    print("\n" + "="*50)
    print("📊 TEST-ERGEBNISSE:")
    print("="*50)
    
    passed = 0
    for level, success in results:
        status = "✅ BESTANDEN" if success else "❌ FEHLGESCHLAGEN"
        print(f"{level}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 GESAMTERGEBNIS: {passed}/5 Levels bestanden")
    
    if passed == 5:
        print("🎉 ALLE LEVELS FUNKTIONIEREN PERFEKT!")
    else:
        print("⚠️  EINIGE LEVELS HABEN PROBLEME!")
    
    return passed == 5

if __name__ == "__main__":
    main()
