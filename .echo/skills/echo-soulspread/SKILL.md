---
name: echo-soulspread
description: Synchronisiert den zentralen System-Config-Ordner (C:\Users\Daddy\.config\echo) in den lokalen Workspace (./.echo) und die zentrale Echo-Konfiguration (C:\Users\Daddy\.echo).
---

# Echo SoulSpread

Dieser Skill betrachtet die globale System-Config (`C:\Users\Daddy\.config\echo\`) als primäre Quelle (Source of Truth) und synchronisiert deren gesamten Inhalt in das aktuell geöffnete Repository (`./.echo/`) sowie in den zentralen Ordner (`C:\Users\Daddy\.echo\`).

## Wann zu verwenden
- Wenn Änderungen an der primären System-Config vorgenommen wurden und sowohl der aktuelle Workspace als auch die zentrale Echo-Konfiguration auf denselben Stand gebracht werden sollen.

## Arbeitsweise
1. **Workspace Sync:** Kopiert `C:\Users\Daddy\.config\echo\*` -> `./.echo/` (überschreibt die lokale Workspace-Instanz).
2. **Central Sync:** Kopiert `C:\Users\Daddy\.config\echo\*` -> `C:\Users\Daddy\.echo\` (überschreibt die zentrale `.echo`-Instanz).

## Skill-Ausführung
Nutze diesen Skill direkt per Tool-Call. Das Skript erkennt den aktuellen Pfad (`Get-Location`) automatisch.
