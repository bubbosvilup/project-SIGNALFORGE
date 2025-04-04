@echo off
cd /d "C:\Users\be_fr\tests"
git commit --allow-empty -m "Commit automatico: %date% %time%"
git push origin main
