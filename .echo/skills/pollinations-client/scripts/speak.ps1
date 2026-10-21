#requires -Version 5.1
<#
.SYNOPSIS
    Synthesize speech via Pollinations and play it immediately.

.DESCRIPTION
    One-shot TTS pipeline: calls pollinations-client.mjs (GET /audio/{text}),
    validates the result, plays it with ffplay (ffmpeg suite) and removes the
    temporary file afterwards.

.EXAMPLE
    .\speak.ps1 -Text "Guten Morgen, Daddy."
    .\speak.ps1 -Text "System online." -Voice nova -Model openai/tts-1 -Keep
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Text,

    [string]$Voice = 'de-DE-Mia',

    [string]$Model = 'microsoft/mai-voice-2.1-flash',

    [string]$OutFile,

    [switch]$Keep
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $PSCommandPath
$client = Join-Path $scriptDir 'pollinations-client.mjs'

if (-not (Test-Path -LiteralPath $client)) {
    throw "pollinations-client.mjs nicht gefunden: $client"
}

if (-not $OutFile) {
    $tempDir = Join-Path $env:TEMP 'echo\tts'
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    $OutFile = Join-Path $tempDir ('echo_tts_{0}.mp3' -f (Get-Date -Format 'yyyyMMdd_HHmmss_fff'))
}

& node $client audio --text $Text --voice $Voice --model $Model --out $OutFile
if ($LASTEXITCODE -ne 0) {
    throw "TTS-Generierung fehlgeschlagen (node exit $LASTEXITCODE)."
}
if (-not (Test-Path -LiteralPath $OutFile)) {
    throw "TTS-Datei wurde nicht erzeugt: $OutFile"
}

$size = (Get-Item -LiteralPath $OutFile).Length
if ($size -lt 2000) {
    $payload = Get-Content -LiteralPath $OutFile -Raw -ErrorAction SilentlyContinue
    throw "TTS-Antwort zu klein ($size Bytes), vermutlich Fehler-Payload: $payload"
}

$stdoutLog = [System.IO.Path]::GetTempFileName()
$stderrLog = [System.IO.Path]::GetTempFileName()
try {
    $player = Start-Process -FilePath 'ffplay.exe' `
        -ArgumentList @('-nodisp', '-autoexit', '-volume', '100', '-loglevel', 'quiet', $OutFile) `
        -Wait -PassThru -NoNewWindow `
        -RedirectStandardOutput $stdoutLog -RedirectStandardError $stderrLog
    $playExit = $player.ExitCode
}
finally {
    Remove-Item -LiteralPath $stdoutLog, $stderrLog -ErrorAction SilentlyContinue
}

if (-not $Keep) {
    Remove-Item -LiteralPath $OutFile -ErrorAction SilentlyContinue
}

if ($playExit -ne 0) {
    throw "ffplay Wiedergabe fehlgeschlagen (exit $playExit)."
}

Write-Output "SPOKEN ($size Bytes, voice=$Voice, model=$Model)"
