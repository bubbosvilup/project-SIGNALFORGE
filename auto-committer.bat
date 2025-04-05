@echo off
cd /d "C:\Users\be_fr\tests"

:: Set chance to commit (0-100). Below this value = commit happens
set threshold=30

:: Generate a random number from 0 to 99
set /a rand=%random% %% 100

:: Skip if random is too high
if %rand% GEQ %threshold% (
    echo [%date% %time%] - Skipped: rand=%rand% >> log-debug.txt
    exit /b
)

:: Randomness chaotic logs quotes
for /f "delims=" %%a in ('powershell -Command ^
    "$subjects = @('EchoUnit', 'DreamCore', 'Subroutine Zeta', 'The ghost in shell', 'EntropyDaemon', 'PixelWraith'); ^
     $verbs = @('whispers', 'transmits', 'forges', 'echoes', 'materializes', 'fractures'); ^
     $objects = @('a silent log', 'an unstable thought', 'a synthetic heartbeat', 'a recursive pulse', 'a phantom commit', 'the last signal'); ^
     $msg = ($subjects | Get-Random) + ' ' + ($verbs | Get-Random) + ' ' + ($objects | Get-Random) + '.'; ^
     Write-Output $msg"') do set commitMsg=%%a

:: Log and push
echo [%date% %time%] - Executed: rand=%rand% - %commitMsg% >> log-debug.txt
git commit --allow-empty -m "%commitMsg%"
git push origin main
