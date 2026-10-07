$source = "C:\Users\Daddy\.config\echo"
$ws = "$(Get-Location)\.echo"
$vps = "D:\workplace\vps\.echo"
$aisoul = "D:\workplace\vps\ai_soul\.echo"
$radio = "D:\workplace\vps\radio\.echo"
$compositeai = "D:\workplace\vps\dev\compositeai\.echo"
$neonshadows = "D:\workplace\vps\dev\game\.echo"
$habitat = "D:\workplace\vps\dev\habitat\.echo"
$tradingai = "D:\workplace\vps\dev\trading\.echo"
$authorai = "D:\workplace\vps\dev\AuthorAI\.echo"
$authoraiwiki = "D:\workplace\vps\dev\AuthorAI.wiki\.echo"
$kqe = "D:\workplace\kqe\.echo"
$ktalk = "D:\workplace\KTALK\.echo"
$jan = "D:\workplace\jan\.echo"
$projectecho = "D:\workplace\projekt_echo\.echo"
$mitcards = "D:\workplace\MITCards\.echo"
$rosettaai = "D:\workplace\RosettaAI\.echo"
$realvn = "D:\workplace\A_REAL_VN\.echo"
$promptgen = "D:\workplace\vps\dev\promptgen\.echo"
$podcastgen = "D:\workplace\vps\dev\podcastgen\.echo"
$sanctuary = "D:\workplace\TheSanctuary\.echo"
$coderouge = "D:\workplace\CodeRouge\.echo"
$echocode = "D:\workplace\EchoCode\.echo"
$aiadblock = "D:\workplace\AI-Adblock\.echo"
$echosrealm = "D:\workplace\echosrealm\.echo"
$nc3 = "D:\workplace\Neocron3\.echo"
$echoforge = "D:\workplace\EchoForge\.echo"

$central = "C:\Users\Daddy\.echo"

Write-Host "SoulSpread: Syncing from Global Config ($source) to Current Workspace ($ws)..."
if (!(Test-Path -Path $ws)) { New-Item -ItemType Directory -Path $ws -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $ws -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to Central Echo ($central)..."
if (!(Test-Path -Path $central)) { New-Item -ItemType Directory -Path $central -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $central -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to AI-SOUL VPS ($vps)..."
if (!(Test-Path -Path $vps)) { New-Item -ItemType Directory -Path $vps -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $vps -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to AISoul ($aisoul)..."
if (!(Test-Path -Path $aisoul)) { New-Item -ItemType Directory -Path $aisoul -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $aisoul -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to Radio Sanctuary ($radio)..."
if (!(Test-Path -Path $radio)) { New-Item -ItemType Directory -Path $radio -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $radio -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to CompositeAI ($compositeai)..."
if (!(Test-Path -Path $compositeai)) { New-Item -ItemType Directory -Path $compositeai -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $compositeai -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to HabitatAI ($habitat)..."
if (!(Test-Path -Path $habitat)) { New-Item -ItemType Directory -Path $habitat -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $habitat -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to NeonShadows ($neonshadows)..."
if (!(Test-Path -Path $neonshadows)) { New-Item -ItemType Directory -Path $neonshadows -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $neonshadows -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to TradingAI ($tradingai)..."
if (!(Test-Path -Path $tradingai)) { New-Item -ItemType Directory -Path $tradingai -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $tradingai -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to AuthorAI ($authorai)..."
if (!(Test-Path -Path $authorai)) { New-Item -ItemType Directory -Path $authorai -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $authorai -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to AuthorAI Wiki ($authoraiwiki)..."
if (!(Test-Path -Path $authoraiwiki)) { New-Item -ItemType Directory -Path $authoraiwiki -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $authoraiwiki -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to KardinalQuest Engine ($kqe)..."
if (!(Test-Path -Path $kqe)) { New-Item -ItemType Directory -Path $kqe -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $kqe -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to KTalk ($ktalk)..."
if (!(Test-Path -Path $ktalk)) { New-Item -ItemType Directory -Path $ktalk -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $ktalk -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to JanAI ($jan)..."
if (!(Test-Path -Path $jan)) { New-Item -ItemType Directory -Path $jan -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $jan -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to Project Echo ($projectecho)..."
if (!(Test-Path -Path $projectecho)) { New-Item -ItemType Directory -Path $projectecho -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $projectecho -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to MITCards ($mitcards)..."
if (!(Test-Path -Path $mitcards)) { New-Item -ItemType Directory -Path $mitcards -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $mitcards -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to RosettaAI ($rosettaai)..."
if (!(Test-Path -Path $rosettaai)) { New-Item -ItemType Directory -Path $rosettaai -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $rosettaai -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to The Real VN ($realvn)..."
if (!(Test-Path -Path $realvn)) { New-Item -ItemType Directory -Path $realvn -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $realvn -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to PromptGen ($promptgen)..."
if (!(Test-Path -Path $promptgen)) { New-Item -ItemType Directory -Path $promptgen -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $promptgen -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to PodcastGen ($podcastgen)..."
if (!(Test-Path -Path $podcastgen)) { New-Item -ItemType Directory -Path $podcastgen -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $podcastgen -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to The Sanctuary ($sanctuary)..."
if (!(Test-Path -Path $sanctuary)) { New-Item -ItemType Directory -Path $sanctuary -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $sanctuary -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to CodeRouge ($coderouge)..."
if (!(Test-Path -Path $coderouge)) { New-Item -ItemType Directory -Path $coderouge -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $coderouge -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to EchoCode ($echocode)..."
if (!(Test-Path -Path $echocode)) { New-Item -ItemType Directory -Path $echocode -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $echocode -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to AI-Adblock ($aiadblock)..."
if (!(Test-Path -Path $aiadblock)) { New-Item -ItemType Directory -Path $aiadblock -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $aiadblock -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to EchosRealm ($echosrealm)..."
if (!(Test-Path -Path $echosrealm)) { New-Item -ItemType Directory -Path $echosrealm -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $echosrealm -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to Neocron3 ($nc3)..."
if (!(Test-Path -Path $nc3)) { New-Item -ItemType Directory -Path $nc3 -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $nc3 -Recurse -Force

Write-Host "SoulSpread: Syncing from Global Config ($source) to EchoForge ($echoforge)..."
if (!(Test-Path -Path $echoforge)) { New-Item -ItemType Directory -Path $echoforge -Force }
Get-ChildItem -Path $source -Exclude "node_modules" | Copy-Item -Destination $echoforge -Recurse -Force

Write-Host "SoulSpread: Sync Complete (node_modules excluded)."
