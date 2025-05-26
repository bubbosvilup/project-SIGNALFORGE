@echo off
>nul chcp 65001
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "C:\Users\be_fr\tests" || (
    echo ERRORE: Cartella non trovata
    pause
    exit /b 1
)
title QUANTUM OBSERVER :: SIGNALFORGE CONTROL CENTER v2.0

:: ================================================================================================
::  ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗
:: ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║
:: ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
:: ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
:: ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
::  ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
::  ██████╗ ██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
:: ██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
:: ██║   ██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
:: ██║   ██║██╔══██╗╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
:: ╚██████╔╝██████╔╝███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
::  ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
:: ================================================================================================
:: SIGNALFORGE Quantum Observer & Control Center v2.0
:: "From the void, we observe. Through observation, we control."
:: ================================================================================================

:: === Initialize Quantum States ===
set mode=monitor
set schedulerActive=0
set schedulerInterval=0
set lastCommitTime=0
set /a quantumCycle=0

:: Check if files exist, create basic structure if needed
if not exist "forge.log" echo [%date% %time%] QUANTUM OBSERVER INITIALIZED > forge.log
if not exist "log-debug.txt" echo QUANTUM OBSERVER - FIRST BOOT > log-debug.txt
if not exist ".forge" mkdir .forge

:: Initialize file timestamps for monitoring
for %%f in (forge.log) do set lastForgeTime=%%~tf
for %%f in (log-debug.txt) do set lastDebugTime=%%~tf

color 0A

:main_interface
cls
call :draw_header
call :check_file_changes
call :draw_status
call :draw_recent_signals
call :draw_scheduler_status
call :draw_menu

:: Input handling
set "choice="
set /p "choice=quantum-observer> "

if /i "!choice!"=="m" set mode=monitor & goto main_interface
if /i "!choice!"=="s" goto scheduler_menu
if /i "!choice!"=="r" goto run_single_commit
if /i "!choice!"=="c" goto config_menu
if /i "!choice!"=="a" goto archive_explorer
if /i "!choice!"=="q" goto quantum_shutdown
if /i "!choice!"=="" goto monitor_cycle

echo [INVALID QUANTUM COMMAND]
timeout /t 1 /nobreak >nul
goto main_interface

:monitor_cycle
:: Check scheduler
if "!schedulerActive!"=="1" (
    call :check_scheduler
)

:: Monitor cycle delay
timeout /t 5 /nobreak >nul
set /a quantumCycle+=1
goto main_interface

:draw_header
echo.
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║                SIGNALFORGE QUANTUM OBSERVER v2.0                     ║
echo  ║                     NEURAL CONTROL CENTER                            ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
goto :eof

:draw_status
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║ QUANTUM FIELD STATUS                                                  ║
echo  ╠═══════════════════════════════════════════════════════════════════════╣

:: Generate random quantum field for demonstration
set /a qField=!RANDOM! %% 100
set /a nPaths=!RANDOM! %% 100
set /a entropy=!RANDOM! %% 100

:: Create bars
set tmp_qField_0=!qField!
call :create_bar %tmp_qField_0% qBar
set tmp_nPaths_1=!nPaths!
call :create_bar %tmp_nPaths_1% nBar
set tmp_entropy_2=!entropy!
call :create_bar %tmp_entropy_2% eBar

echo  ║ QUANTUM DENSITY:    [!qBar!] !qField!/100                  ║
echo  ║ NEURAL PATHWAYS:    [!nBar!] !nPaths!/100                  ║
echo  ║ ENTROPY LEVELS:     [!eBar!] !entropy!/100                 ║
echo  ║                                                                   ║
echo  ║ OBSERVER CYCLES:    !quantumCycle!                                        ║
echo  ║ SYSTEM TIME:        !date! !time:~0,8!                          ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
goto :eof

:create_bar
set /a barLength=%1/5
set tempBar=
for /l %%i in (1,1,!barLength!) do set tempBar=!tempBar!█
for /l %%i in (!barLength!,1,19) do set tempBar=!tempBar!░
set "%2=!tempBar!"
goto :eof

:draw_recent_signals
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║ RECENT SIGNAL MANIFESTATIONS                                          ║
echo  ╠═══════════════════════════════════════════════════════════════════════╣

if exist forge.log (
    echo  ║                                                                   ║
    for /f "usebackq delims=" %%a in (`powershell -command "if (Test-Path 'forge.log') { Get-Content 'forge.log' -Tail 3 }"`) do call :print_log_line "%%a"
    )
    echo  ║                                                                   ║
) else (
    echo  ║                                                                   ║
    echo  ║               NO SIGNALS DETECTED - QUANTUM VOID                  ║
    echo  ║                                                                   ║
)

echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
goto :eof

:draw_scheduler_status
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║ AUTO-COMMITTER SCHEDULER STATUS                                       ║
echo  ╠═══════════════════════════════════════════════════════════════════════╣

if !schedulerActive!==1 (
    echo  ║ STATUS: 🟢 ACTIVE - QUANTUM FIELD MONITORING                       ║
    echo  ║ INTERVAL: !schedulerInterval! MINUTES                                      ║
    
    :: Calculate next execution time
    set /a timeLeft=!schedulerInterval!-!elapsedMinutes!
    if !timeLeft! lss 0 set timeLeft=0
    echo  ║ NEXT EXECUTION: ~!timeLeft! MINUTES                                  ║
) else (
    echo  ║ STATUS: 🔴 INACTIVE - MANUAL CONTROL MODE                          ║
    echo  ║ SCHEDULER: QUANTUM FIELD DORMANT                                  ║
)

echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
goto :eof

:draw_menu
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║ QUANTUM CONTROL COMMANDS                                              ║
echo  ╠═══════════════════════════════════════════════════════════════════════╣
echo  ║                                                                       ║
echo  ║  [M] MONITOR MODE - Continue monitoring quantum fields                ║
echo  ║  [S] SCHEDULER - Configure auto-committer timing                      ║
echo  ║  [R] RUN NOW - Execute single commit immediately                      ║
echo  ║  [C] CONFIG - Quantum parameter configuration                         ║
echo  ║  [A] ARCHIVE - Explore dimensional data archives                      ║
echo  ║  [Q] QUIT - Shutdown quantum observer                                 ║
echo  ║                                                                       ║
echo  ║  [ENTER] Continue monitoring cycle...                                 ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
goto :eof

:check_file_changes
:: Check if forge.log changed
if exist forge.log (
    for %%f in (forge.log) do set "currentForgeTime=%%~tf"
    if not "!currentForgeTime!"=="!lastForgeTime!" (
        set "lastForgeTime=!currentForgeTime!"
        rem File changed - could add visual indicator here
    )
)

:: Check if log-debug.txt changed
if exist log-debug.txt (
    for %%f in (log-debug.txt) do set "currentDebugTime=%%~tf"
    if not "!currentDebugTime!"=="!lastDebugTime!" (
        set "lastDebugTime=!currentDebugTime!"
    )
)
goto :eof

:scheduler_menu
cls
call :draw_header
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║ AUTO-COMMITTER SCHEDULER CONFIGURATION                                ║
echo  ╠═══════════════════════════════════════════════════════════════════════╣
echo  ║                                                                       ║
echo  ║  [1] Every 15 minutes - High frequency quantum pulses                 ║
echo  ║  [2] Every 30 minutes - Standard neural rhythm                        ║
echo  ║  [3] Every 60 minutes - Deep meditation cycle                         ║
echo  ║  [4] Every 120 minutes - Extended quantum contemplation               ║
echo  ║  [5] Custom interval - Define your own temporal pattern               ║
echo  ║  [6] Smart mode - Adaptive random intervals (30-90 min)              ║
echo  ║                                                                       ║
if !schedulerActive!==1 (
    echo  ║  [0] STOP SCHEDULER - Deactivate auto-committer                       ║
)
echo  ║  [B] BACK - Return to main observer                                   ║
echo  ║                                                                       ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.

set /p schedChoice=scheduler:~$ 

if "!schedChoice!"=="1" call :set_scheduler 15 & goto main_interface
if "!schedChoice!"=="2" call :set_scheduler 30 & goto main_interface  
if "!schedChoice!"=="3" call :set_scheduler 60 & goto main_interface
if "!schedChoice!"=="4" call :set_scheduler 120 & goto main_interface
if "!schedChoice!"=="5" goto custom_interval
if "!schedChoice!"=="6" call :set_scheduler_smart & goto main_interface
if "!schedChoice!"=="0" call :stop_scheduler & goto main_interface
if /i "!schedChoice!"=="b" goto main_interface

echo [INVALID SCHEDULER COMMAND]
timeout /t 1 /nobreak >nul
goto scheduler_menu

:custom_interval
echo.
set /p customMin=Enter interval in minutes (5-1440): 
if !customMin! geq 5 if !customMin! leq 1440 (
    call :set_scheduler !customMin!
    goto main_interface
) else (
    echo Invalid interval. Must be between 5 and 1440 minutes.
    timeout /t 2 /nobreak >nul
    goto scheduler_menu
)

:set_scheduler
set schedulerActive=1
set schedulerInterval=%1
set schedulerStartTime=!time!
set elapsedMinutes=0
echo [%date% %time%] SCHEDULER ACTIVATED: %1 minutes interval >> forge.log
goto :eof

:set_scheduler_smart  
set schedulerActive=1
set /a schedulerInterval=30+(!RANDOM! %% 60)
set schedulerStartTime=!time!
set elapsedMinutes=0
echo [%date% %time%] SMART SCHEDULER ACTIVATED: !schedulerInterval! minutes (adaptive) >> forge.log
goto :eof

:stop_scheduler
set schedulerActive=0
set schedulerInterval=0
echo [%date% %time%] SCHEDULER DEACTIVATED >> forge.log
goto :eof

:check_scheduler
:: Simple time check - in a real implementation you'd want more precise timing
set /a elapsedMinutes+=1
if !elapsedMinutes! geq !schedulerInterval! (
    echo [%date% %time%] EXECUTING SCHEDULED COMMIT... >> forge.log
    if exist auto-committer.bat call auto-committer.bat
    set elapsedMinutes=0
    
    :: If smart mode, generate new random interval
    if !schedulerInterval! geq 30 if !schedulerInterval! leq 90 (
        set /a schedulerInterval=30+(!RANDOM! %% 60)
    )
)
goto :eof

:run_single_commit
cls
call :draw_header
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║                    MANUAL SIGNAL MANIFESTATION                        ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo  [%date% %time%] Initiating manual quantum commit...
echo.

if exist auto-committer.bat (
    call auto-committer.bat
) else (
    echo  ERROR: auto-committer.bat not found in current directory.
)

echo.
echo  [%date% %time%] Manual commit execution completed.
echo  Press any key to return to observer...
pause >nul
goto main_interface

:config_menu
cls
call :draw_header
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║                    QUANTUM CONFIGURATION                              ║
echo  ╠═══════════════════════════════════════════════════════════════════════╣
echo  ║                                                                       ║
echo  ║  Configuration options will be implemented in future updates          ║
echo  ║  Current focus: Core monitoring and scheduling functions              ║
echo  ║                                                                       ║
echo  ║  Planned features:                                                    ║
echo  ║  • Quantum threshold adjustment                                       ║
echo  ║  • Neural pathway calibration                                         ║
echo  ║  • Entropy level modification                                         ║
echo  ║  • Signal frequency tuning                                            ║
echo  ║                                                                       ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo  Press any key to return...
pause >nul
goto main_interface

:archive_explorer
cls
call :draw_header
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║                    DIMENSIONAL ARCHIVE EXPLORER                       ║
echo  ╠═══════════════════════════════════════════════════════════════════════╣

if exist master-quantum-log.txt (
    echo  ║                                                                       ║
    echo  ║ LAST 10 QUANTUM MANIFESTATIONS:                                      ║
    echo  ║                                                                       ║
    
    for /f "usebackq delims=" %%a in (`powershell -command "if ^(Test-Path master-quantum-log.txt^) { Get-Content master-quantum-log.txt -Tail 10 }"`) do (
        set "line=%%a"
        set "shortLine=!line:~0,65!"
        echo  ║ !shortLine!... ║
    )
) else (
    echo  ║                                                                       ║
    echo  ║               NO ARCHIVE DATA AVAILABLE                               ║
    echo  ║                                                                       ║
)

echo  ║                                                                       ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo  Press any key to return...
pause >nul
goto main_interface

:quantum_shutdown
cls
call :draw_header
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║                      QUANTUM SHUTDOWN SEQUENCE                        ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo  [%date% %time%] Initiating quantum field collapse...
timeout /t 1 /nobreak >nul
echo  [%date% %time%] Disconnecting neural pathways...
timeout /t 1 /nobreak >nul
echo  [%date% %time%] Storing quantum states...
timeout /t 1 /nobreak >nul
echo  [%date% %time%] Observer shutdown complete.
echo.
echo  "The void observes those who observe the void."
echo.
timeout /t 3 /nobreak >nul
pause
exit /b

:print_log_line
set "line=%~1"
if not "%line%"=="" (
    setlocal enabledelayedexpansion
    set "shortLine=!line:~0,65!"
    echo  ║ !shortLine!... ║
    endlocal
)
goto :eof