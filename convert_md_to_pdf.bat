@echo off
pushd %~dp0
python md_to_pdf.py
popd
pause
