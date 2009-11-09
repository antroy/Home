; Name of the installer (don't really care here because of silent below)
!define VER "0.0.0.1"

Name "${FULLNAME}"
 
; Don't want a window, just unpack files and execute
SilentInstall silent
 
; Set a name for the resulting executable
OutFile "${NAME}.exe"
 
Caption "${FULLNAME}"
VIProductVersion "${VER}"
VIAddVersionKey ProductName "${FULLNAME}"
VIAddVersionKey FileDescription "${FULLNAME}"
VIAddVersionKey InternalName "${FULLNAME}"
VIAddVersionKey LegalCopyright "PortableApps.com"
VIAddVersionKey ProductVersion "${VER}"
VIAddVersionKey FileVersion "${VER}"

; Set an icon (optional)
Icon "${ICON}"

; The command to run
Section ""
  SetOutPath '$EXEDIR\App'
  ExecWait '$EXEDIR\App\$EXEFILE'
SectionEnd


