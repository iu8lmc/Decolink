# Verifica che il pacchetto funzioni su un PC SENZA Qt/MSYS2: avvia l'exe con
# un PATH ripulito e ne riporta l'esito. Provarlo da una shell che ha MSYS2 nel
# PATH non dimostra niente, perche' Windows ripesca da li' le librerie mancanti.
param([Parameter(Mandatory=$true)][string]$Exe)

$dir = Split-Path $Exe -Parent
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $Exe
$psi.Arguments = "--selftest"
$psi.WorkingDirectory = $dir
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.EnvironmentVariables["PATH"] = "C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem"

$p = [System.Diagnostics.Process]::Start($psi)
$out = $p.StandardOutput.ReadToEnd()
$err = $p.StandardError.ReadToEnd()
if (-not $p.WaitForExit(30000)) { $p.Kill(); Write-Output "TIMEOUT"; exit 9 }

if ($out) { Write-Output $out.Trim() }
if ($err) { Write-Output $err.Trim() }
if ($p.ExitCode -ne 0) {
    Write-Output ("codice di uscita: {0} (0x{1:X8})" -f $p.ExitCode, $p.ExitCode)
    if ($p.ExitCode -eq -1073741515) { Write-Output "= libreria mancante nel pacchetto" }
}
exit $p.ExitCode
