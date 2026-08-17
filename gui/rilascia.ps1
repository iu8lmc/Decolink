# rilascia.ps1 — dal sorgente ai due pacchetti firmati, in un comando.
#
#   .\rilascia.ps1                 compila, firma, crea installer e zip
#   .\rilascia.ps1 -SaltaCompila   riusa l'eseguibile gia' compilato
#   .\rilascia.ps1 -SenzaFirma     salta la firma (utile su una macchina senza certificato)
#
# La versione non si passa: si legge da CMakeLists.txt, che e' l'unico posto
# dove sta scritta. Cosi' non esiste il caso in cui l'installer dice una
# versione e l'eseguibile un'altra.

[CmdletBinding()]
param(
    [switch]$SaltaCompila,
    [switch]$SenzaFirma
)

$ErrorActionPreference = 'Stop'
$qui     = Split-Path -Parent $MyInvocation.MyCommand.Path
$radice  = Split-Path -Parent $qui
$build   = Join-Path $qui 'build'
$dist    = Join-Path $radice 'dist'
$cartella = Join-Path $dist 'Decolink'

function Passo($t) { Write-Host "`n=== $t" -ForegroundColor Cyan }
function Nota($t)  { Write-Host "    $t" -ForegroundColor DarkGray }

# ---------------------------------------------------------------- la versione
$cm = Get-Content (Join-Path $qui 'CMakeLists.txt') -Raw
if ($cm -notmatch 'project\(decolink\s+VERSION\s+([0-9]+\.[0-9]+\.[0-9]+)') {
    throw "versione non trovata in CMakeLists.txt"
}
$versione = $Matches[1]
Passo "Decolink $versione"

# ---------------------------------------------------------------- gli attrezzi
$mingw = 'C:\msys64\mingw64\bin'
$iscc  = @("${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
           "$env:ProgramFiles\Inno Setup 6\ISCC.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $iscc) { throw "Inno Setup 6 non trovato: serve ISCC.exe" }

$signtool = $null
if (-not $SenzaFirma) {
    $signtool = Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin" -Filter signtool.exe -Recurse -ErrorAction SilentlyContinue |
                Where-Object { $_.FullName -like '*\x64\*' } | Sort-Object FullName -Descending |
                Select-Object -First 1 -ExpandProperty FullName
    if (-not $signtool) { Write-Warning "signtool non trovato: si prosegue senza firmare"; $SenzaFirma = $true }
}

$impronta = $null
if (-not $SenzaFirma) {
    $cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert |
            Where-Object { $_.HasPrivateKey -and $_.NotAfter -gt (Get-Date) } |
            Sort-Object NotAfter -Descending | Select-Object -First 1
    if (-not $cert) { Write-Warning "nessun certificato di firma valido: si prosegue senza firmare"; $SenzaFirma = $true }
    else {
        $impronta = $cert.Thumbprint
        Nota "firma con: $($cert.Subject)  (scade $($cert.NotAfter.ToString('dd/MM/yyyy')))"
        if ($cert.Subject -eq $cert.Issuer) {
            Nota "il certificato e' autofirmato: garantisce integrita' e identita',"
            Nota "ma su altri computer Windows dira' comunque «editore sconosciuto»."
        }
    }
}

function Firma([string]$file, [string]$descrizione) {
    if ($SenzaFirma) { return }
    # Marca temporale: senza, la firma smette di valere il giorno in cui scade
    # il certificato, anche sui file gia' distribuiti.
    & $signtool sign /sha1 $impronta /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 `
        /d $descrizione /du 'https://decolink.ft2.it' $file | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "firma fallita: $file" }
    Nota "firmato: $(Split-Path -Leaf $file)"
}

# ---------------------------------------------------------------- compilazione
if (-not $SaltaCompila) {
    Passo "Compilazione"
    $env:PATH = "$mingw;$env:PATH"
    & (Join-Path $mingw 'cmake.exe') --build $build -j 4 2>&1 | Select-String -Pattern 'error|Built target' | ForEach-Object { Nota $_ }
    if ($LASTEXITCODE -ne 0) { throw "compilazione fallita" }
}

$exe = Join-Path $build 'decolink.exe'
if (-not (Test-Path $exe)) { throw "manca $exe" }

# La versione dichiarata dall'eseguibile deve essere quella che stiamo
# rilasciando: se non torna, da qualche parte c'e' una build vecchia.
$vExe = (Get-Item $exe).VersionInfo.FileVersion
if ($vExe -ne $versione) { throw "l'eseguibile dice $vExe ma stiamo rilasciando $versione" }
Nota "l'eseguibile dichiara la versione $vExe"

# ---------------------------------------------------------------- il pacchetto
Passo "Pacchetto"
Copy-Item $exe (Join-Path $cartella 'Decolink.exe') -Force
Nota "eseguibile aggiornato in dist\Decolink"
Firma (Join-Path $cartella 'Decolink.exe') 'Decolink'

# ---------------------------------------------------------------- l'installer
Passo "Installer"
& $iscc "/DVersione=$versione" "/DSorgente=$cartella" "/DUscita=$dist" (Join-Path $qui 'decolink.iss') | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Inno Setup ha fallito" }
$installer = Join-Path $dist "Decolink-$versione-installa.exe"
if (-not (Test-Path $installer)) { throw "installer non prodotto" }
Nota "$([Math]::Round((Get-Item $installer).Length / 1MB, 1)) MB"
Firma $installer "Installazione di Decolink $versione"

# ---------------------------------------------------------------- lo zip
Passo "Archivio portatile"
$zip = Join-Path $dist 'Decolink-windows-x64.zip'
Remove-Item $zip -ErrorAction SilentlyContinue
$sevenzip = 'C:\msys64\usr\bin\7z.exe'
if (Test-Path $sevenzip) {
    & $sevenzip a -tzip -mx=7 $zip $cartella | Out-Null
} else {
    Compress-Archive -Path $cartella -DestinationPath $zip -CompressionLevel Optimal -Force
}
Nota "$([Math]::Round((Get-Item $zip).Length / 1MB, 1)) MB"

# ---------------------------------------------------------------- riepilogo
Passo "Fatto"
Get-ChildItem $installer, $zip | ForEach-Object {
    $f = if ($SenzaFirma) { '' } else { (Get-AuthenticodeSignature $_.FullName).Status }
    "{0,-42} {1,8:N1} MB  {2}" -f $_.Name, ($_.Length / 1MB), $f
}
""
"Da pubblicare:"
"  gh release create v$versione `"$installer`" `"$zip`" --repo iu8lmc/Decolink --title `"Decolink v$versione`" --notes-file NOTE.md"
