@echo off 

python setup.py py2exe -b 1

rem cd dist

rem "C:\Program Files\7-Zip\7z.exe" -aoa x library.zip -olibrary\ 
rem del library.zip 
 
rem cd library\ 
rem "C:\Program Files\7-Zip\7z.exe" a -tzip -mx9 ..\library.zip -r 
rem cd.. 
rem rd library /s /q 
 
rem "C:\ant\bin\upx.exe" --best *.*


