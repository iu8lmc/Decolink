# Verifica che il pacchetto funzioni su un PC SENZA Qt/MSYS2: avvia l'exe con un
# PATH ripulito e ne riporta l'esito. Provarlo da una shell che ha MSYS2 nel PATH
# non dimostra niente, perche' Windows ripesca da li' le librerie mancanti.
#
# Si provano tre cose, perche' ognuna carica librerie diverse e una sola non
# basta a dire che il pacchetto e' completo:
#
#   --selftest    apre l'ingresso audio e cattura mezzo secondo (backend Qt
#                 Multimedia, che tira dentro ffmpeg e i suoi codec)
#   --codectest   comprime e decomprime con Opus (libopus)
#   --emrgtest    modem e voce del collegamento d'emergenza (libcodec2)
#
# Senza le ultime due un pacchetto senza libopus o libcodec2 sembrerebbe valido:
# l'audio parte, e il guasto si scoprirebbe solo quando qualcuno prova a
# collegarsi davvero.
param([Parameter(Mandatory = $true)][string]$Exe)

$dir = Split-Path $Exe -Parent
$pulito = "C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem"

function Prova {
    param([string]$Argomenti, [int]$TimeoutMs, [switch]$Facoltativa)

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $Exe
    $psi.Arguments = $Argomenti
    $psi.WorkingDirectory = $dir
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.EnvironmentVariables["PATH"] = $pulito

    $p = [System.Diagnostics.Process]::Start($psi)
    $out = $p.StandardOutput.ReadToEnd()
    $err = $p.StandardError.ReadToEnd()
    if (-not $p.WaitForExit($TimeoutMs)) {
        $p.Kill()
        Write-Host "  $Argomenti : TIMEOUT"
        return 9
    }
    $codice = $p.ExitCode

    # Write-Host e non Write-Output: dentro una funzione che restituisce un
    # valore, Write-Output finisce nella variabile del chiamante invece che a
    # schermo, e il codice di uscita diventa un array. Difetto scoperto quando
    # questa verifica ha smesso di stampare qualunque cosa pur "passando".
    if ($codice -eq 0) {
        Write-Host "  $Argomenti : OK"
    } else {
        Write-Host ("  {0} : codice {1} (0x{2:X8})" -f $Argomenti, $codice, $codice)
        if ($codice -eq -1073741515) {
            Write-Host "      = libreria mancante nel pacchetto"
        }
        if ($Facoltativa -and $codice -eq 3) {
            # 3 = compilato senza libcodec2: il pacchetto e' valido, semplicemente
            # non ha il collegamento d'emergenza.
            Write-Host "      = compilato senza libcodec2 (emergenza non disponibile)"
            return 0
        }
        foreach ($riga in ($out + $err).Split("`n")) {
            if ($riga.Trim()) { Write-Host "      $($riga.Trim())" }
        }
    }
    return $codice
}

$esito = 0

$r = Prova -Argomenti "--selftest" -TimeoutMs 30000
if ($r -ne 0) { $esito = $r }

$r = Prova -Argomenti "--codectest" -TimeoutMs 120000
if ($r -ne 0 -and $esito -eq 0) { $esito = $r }

$r = Prova -Argomenti "--emrgtest" -TimeoutMs 180000 -Facoltativa
if ($r -ne 0 -and $esito -eq 0) { $esito = $r }

# Hamlib: apre la radio finta e le comanda frequenza, modo e PTT. Senza questa
# prova, un pacchetto a cui manca libhamlib sembrerebbe valido finche' qualcuno
# non prova a collegare una radio.
$r = Prova -Argomenti "--hamlibtest" -TimeoutMs 120000 -Facoltativa
if ($r -ne 0 -and $esito -eq 0) { $esito = $r }

exit $esito
