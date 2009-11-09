; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=IP Address Finder
AppVerName=IP Address Finder 1.0
AppPublisher=Antroy Software
DefaultDirName={pf}\IP Address Finder
DefaultGroupName=IP Address Finder
AllowNoIcons=yes
OutputDir="E:\svn\svn-trunk\Python\sandbox\display_ipaddress\installer\"
OutputBaseFilename="IP Address Finder Setup"
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "E:\svn\svn-trunk\Python\sandbox\display_ipaddress\dist\ip-address.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\svn\svn-trunk\Python\sandbox\display_ipaddress\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\IP Address Finder"; Filename: "{app}\ip-address.exe"
Name: "{group}\{cm:UninstallProgram,IP Address Finder}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\IP Address Finder"; Filename: "{app}\ip-address.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\ip-address.exe"; Description: "{cm:LaunchProgram,IP Address Finder}"; Flags: nowait postinstall skipifsilent
