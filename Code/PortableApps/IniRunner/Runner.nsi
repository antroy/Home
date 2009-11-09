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
;Icon "R.ico"
Icon "${ICON}"

Function StrStr
   Exch $R1
   Exch    
   Exch $R2
   Push $R3
   Push $R4
   Push $R5
   StrLen $R3 $R1
   StrCpy $R4 0

   loop:
     StrCpy $R5 $R2 $R3 $R4
     StrCmp $R5 $R1 done
     StrCmp $R5 "" done
     IntOp $R4 $R4 + 1
     Goto loop
 done:
   StrCpy $R1 $R2 "" $R4
   Pop $R5
   Pop $R4
   Pop $R3
   Pop $R2
   Exch $R1
 FunctionEnd


; The command to run
Section ""
  StrCpy $R9 $EXEFILE -4

  ReadINIStr $R1 "$EXEDIR\runner.ini" "$R9" "exe"
  ReadINIStr $R2 "$EXEDIR\runner.ini" "$R9" "args"

; This needs to be more robust!!
  Push $CMDLINE
  Push $R9

  Call StrStr

  Pop $R0
  Push $R0
  Push " "

  Call StrStr
  Pop $R0

  Exec '"$R1" $R2 $R0'
SectionEnd


