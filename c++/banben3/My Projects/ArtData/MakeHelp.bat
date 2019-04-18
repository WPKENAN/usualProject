@echo off
REM -- First make map file from Microsoft Visual C++ generated resource.h
echo // MAKEHELP.BAT generated Help Map file.  Used by ARTDATA.HPJ. >"hlp\ArtData.hm"
echo. >>"hlp\ArtData.hm"
echo // Commands (ID_* and IDM_*) >>"hlp\ArtData.hm"
makehm ID_,HID_,0x10000 IDM_,HIDM_,0x10000 resource.h >>"hlp\ArtData.hm"
echo. >>"hlp\ArtData.hm"
echo // Prompts (IDP_*) >>"hlp\ArtData.hm"
makehm IDP_,HIDP_,0x30000 resource.h >>"hlp\ArtData.hm"
echo. >>"hlp\ArtData.hm"
echo // Resources (IDR_*) >>"hlp\ArtData.hm"
makehm IDR_,HIDR_,0x20000 resource.h >>"hlp\ArtData.hm"
echo. >>"hlp\ArtData.hm"
echo // Dialogs (IDD_*) >>"hlp\ArtData.hm"
makehm IDD_,HIDD_,0x20000 resource.h >>"hlp\ArtData.hm"
echo. >>"hlp\ArtData.hm"
echo // Frame Controls (IDW_*) >>"hlp\ArtData.hm"
makehm IDW_,HIDW_,0x50000 resource.h >>"hlp\ArtData.hm"
REM -- Make help for Project ARTDATA


echo Building Win32 Help files
start /wait hcw /C /E /M "hlp\ArtData.hpj"
if errorlevel 1 goto :Error
if not exist "hlp\ArtData.hlp" goto :Error
if not exist "hlp\ArtData.cnt" goto :Error
echo.
if exist Debug\nul copy "hlp\ArtData.hlp" Debug
if exist Debug\nul copy "hlp\ArtData.cnt" Debug
if exist Release\nul copy "hlp\ArtData.hlp" Release
if exist Release\nul copy "hlp\ArtData.cnt" Release
echo.
goto :done

:Error
echo hlp\ArtData.hpj(1) : error: Problem encountered creating help file

:done
echo.
