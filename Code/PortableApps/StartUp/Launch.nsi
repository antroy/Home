; Name of the installer (don't really care here because of silent below)
!define VER "0.0.0.1"
!define FULLNAME "Application Runner"

Name "AppRunner"
 
; Don't want a window, just unpack files and execute
SilentInstall silent
;ShowInstDetails show
 
; Set a name for the resulting executable
OutFile "StartPortableApps.exe"
 
Caption "${FULLNAME}"
VIProductVersion "${VER}"
VIAddVersionKey ProductName "${FULLNAME}"
VIAddVersionKey FileDescription "${FULLNAME}"
VIAddVersionKey InternalName "${FULLNAME}"
VIAddVersionKey LegalCopyright "PortableApps.com"
VIAddVersionKey ProductVersion "${VER}"
VIAddVersionKey FileVersion "${VER}"

; Set an icon (optional)
Icon "favicon.ico"

; The command to run
Section ""
  EnumINI::SectionNames "$EXEDIR\startup.ini"
  Pop $R1
  StrCmp $R1 "error" done
  loop:
    IntCmp $R1 "0" done done 0
    Pop $R2
    ReadINIStr $R3 "$EXEDIR\startup.ini" "$R2" "dir"
    ReadINIStr $R4 "$EXEDIR\startup.ini" "$R2" "file"
    
    StrCpy $R9 $R3 2 1
    DetailPrint "PathSep: $R9"

    StrCpy $R8 ""

    StrCmp $R9 ":\" abspath
    StrCpy $R8 "$EXEDIR\"

    abspath:
    SetOutPath '$R8$R3'

    DetailPrint "pwd: $OUTDIR"
    Exec "$R4"
    IntOp $R1 $R1 - 1
    Goto loop
  done:
  DetailPrint ""
    
SectionEnd



