; decolink.iss — l'installer di Decolink, per Inno Setup 6.
;
; Sostituisce lo zip da scompattare a mano: mette il programma in Programmi,
; crea i collegamenti, registra la voce per «Installazione applicazioni» e sa
; disinstallarsi. Chi preferisce la cartella portatile trova ancora lo zip
; accanto, nella stessa release.
;
; La versione non e' scritta qui: la passa lo script di rilascio con
;     ISCC.exe /DVersione=2.3.0 /DSorgente=..\dist\Decolink decolink.iss
; cosi' esiste un solo posto al mondo dove sta scritta, ed e' CMakeLists.txt.

#ifndef Versione
  #define Versione "0.0.0"
#endif
#ifndef Sorgente
  #define Sorgente "..\dist\Decolink"
#endif
#ifndef Uscita
  #define Uscita "..\dist"
#endif

#define Nome      "Decolink"
#define Autore    "IU8LMC - Martino Merola"
#define Sito      "https://decolink.ft2.it"
#define Eseguibile "Decolink.exe"

[Setup]
; L'AppId non cambia mai: e' quello che lega un aggiornamento all'installazione
; gia' presente. Cambiarlo vorrebbe dire ritrovarsi due Decolink installati.
AppId={{7B3A9C42-5E18-4D6B-9F27-DC0A1E4B8F63}
AppName={#Nome}
AppVersion={#Versione}
AppVerName={#Nome} {#Versione}
AppPublisher={#Autore}
AppPublisherURL={#Sito}
AppSupportURL={#Sito}
AppUpdatesURL={#Sito}
VersionInfoVersion={#Versione}
VersionInfoProductName={#Nome}
VersionInfoCompany={#Autore}
VersionInfoDescription=Installazione di {#Nome}

DefaultDirName={autopf}\{#Nome}
DefaultGroupName={#Nome}
DisableProgramGroupPage=yes
; Niente pagina «pronto per installare»: le scelte sono due, e farle confermare
; una seconda volta e' solo un clic in piu'.
DisableReadyPage=yes
LicenseFile=
InfoBeforeFile=
OutputDir={#Uscita}
OutputBaseFilename=Decolink-{#Versione}-installa
SetupIconFile={#Sorgente}\hfgw.ico
UninstallDisplayIcon={app}\{#Eseguibile}
UninstallDisplayName={#Nome} {#Versione}

; Si installa per l'utente corrente se non ci sono i diritti di amministratore.
; Chiedere l'elevazione per un programma che non tocca niente del sistema e' un
; ostacolo in piu' su un computer di stazione, dove spesso non si e' amministratori.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0

[Languages]
Name: "it";    MessagesFile: "compiler:Languages\Italian.isl"
Name: "en";    MessagesFile: "compiler:Default.isl"
Name: "de";    MessagesFile: "compiler:Languages\German.isl"
Name: "fr";    MessagesFile: "compiler:Languages\French.isl"
Name: "es";    MessagesFile: "compiler:Languages\Spanish.isl"
Name: "pt";    MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "nl";    MessagesFile: "compiler:Languages\Dutch.isl"
Name: "ca";    MessagesFile: "compiler:Languages\Catalan.isl"
Name: "da";    MessagesFile: "compiler:Languages\Danish.isl"
Name: "hu";    MessagesFile: "compiler:Languages\Hungarian.isl"
Name: "ru";    MessagesFile: "compiler:Languages\Russian.isl"
Name: "ja";    MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Tutta la cartella distribuibile: l'eseguibile, le DLL di Qt e delle librerie,
; i plugin nelle loro sottocartelle e le traduzioni di Qt.
Source: "{#Sorgente}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#Nome}";            Filename: "{app}\{#Eseguibile}"
Name: "{group}\{cm:UninstallProgram,{#Nome}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#Nome}";      Filename: "{app}\{#Eseguibile}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#Eseguibile}"; Description: "{cm:LaunchProgram,{#Nome}}"; \
    Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Le impostazioni restano nel registro: chi disinstalla per reinstallare non
; deve riscrivere host, porta e profilo. Si tolgono solo i file nostri.
Type: filesandordirs; Name: "{app}\translations"
Type: dirifempty;     Name: "{app}"

[Code]
// Se Decolink e' in esecuzione, i file sono occupati e l'installazione
// fallirebbe a meta'. Meglio dirlo prima e lasciar chiudere.
function InitializeSetup(): Boolean;
var
  inEsecuzione: Boolean;
  esito: Integer;
begin
  Result := True;
  inEsecuzione := CheckForMutexes('DecolinkInEsecuzione');
  if not inEsecuzione then
    Exit;
  esito := MsgBox('Decolink è aperto. Chiudilo prima di continuare, altrimenti '
                  + 'i file in uso non possono essere sostituiti.' + #13#10#13#10
                  + 'Riprovo?', mbConfirmation, MB_RETRYCANCEL);
  if esito = IDRETRY then
    Result := InitializeSetup()
  else
    Result := False;
end;
