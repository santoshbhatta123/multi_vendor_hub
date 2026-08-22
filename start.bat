@echo off
cd /d C:\multi_vendor_hub
call conda activate multivendor
python create_admin.py
if %errorlevel% neq 0 pause
python run.py
pause
