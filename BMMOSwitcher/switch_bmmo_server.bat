@echo off
echo BMMO Server Switcher

echo 1 - CN Main BMMO Srv
echo 2 - CN Sub BMMO Srv
echo 3 - Discord BMMO Srv

set /p srv="Your choice: "

set "dest=ModLoader\Config\BallanceMMOClient.cfg"
if "%srv%"=="1" (
set "orig=BMMOCfgs\CN1.cfg"
) else if "%srv%"=="2" (
set orig=BMMOCfgs\CN2.cfg"
) else if "%srv%"=="3" (
set "orig=BMMOCfgs\DC.cfg"
) else (
echo No matched server, select CN Sub BMMO Srv by default.
set "orig=BMMOCfgs\CN2.cfg"
)

echo Copying %orig% to %dest%
copy %orig% %dest%
if %errorlevel% equ 0 (
echo Switch OK.
) else (
echo Operation fail. Press any key to exit.
)

pause
