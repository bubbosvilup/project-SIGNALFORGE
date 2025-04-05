@echo off
setlocal enabledelayedexpansion
cd /d "C:\Users\be_fr\tests"

:: === Config ===
set threshold=35

:: === Rotate log once a week (on Sunday) ===
for /f %%d in ('powershell -command "(Get-Date).DayOfWeek"') do set day=%%d
if /i "!day!"=="Sunday" (
    if exist log-debug.txt (
        copy log-debug.txt log-!date:~-4!!date:~3,2!!date:~0,2!.txt > nul
        del log-debug.txt
    )
)

:: === Random roll ===
set /a rand=!random! %% 100
if !rand! GEQ !threshold! (
    echo [%date% %time%] - Skipped: rand=!rand! >> log-debug.txt
    exit /b
)

:: === Word banks ===
set /a subjectIndex=!random! %% 10
set /a verbIndex=!random! %% 10
set /a objectIndex=!random! %% 10

:: === Subjects ===
set subject0=EchoUnit
set subject1=DreamCore
set subject2=Subroutine Zeta
set subject3=The ghost in shell
set subject4=EntropyDaemon
set subject5=PixelWraith
set subject6=GlitchDrive
set subject7=NeuroSpark
set subject8=Protocol Nova
set subject9=Anomaly Thread

:: === Verbs ===
set verb0=whispers
set verb1=transmits
set verb2=forges
set verb3=echoes
set verb4=materializes
set verb5=fractures
set verb6=executes
set verb7=spawns
set verb8=compiles
set verb9=distorts

:: === Objects ===
set object0=a silent log
set object1=an unstable thought
set object2=a synthetic heartbeat
set object3=a recursive pulse
set object4=a phantom commit
set object5=the last signal
set object6=a corrupted frame
set object7=a quantum blink
set object8=a forbidden echo
set object9=an ephemeral byte

:: === Build commit message ===
set commitMsg=!subject%subjectIndex%! !verb%verbIndex%! !object%objectIndex%!.

:: === Log and commit ===
echo [%date% %time%] - Executed: rand=!rand! - !commitMsg! >> log-debug.txt
git commit --allow-empty -m "!commitMsg!"
git push origin main
