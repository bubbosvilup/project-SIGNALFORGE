@echo off
cd /d "C:\Users\be_fr\tests"
echo Script avviato %date% %time% >> log-debug.txt
git commit --allow-empty -m "Commit automatico: %date% %time%"
git push origin main
