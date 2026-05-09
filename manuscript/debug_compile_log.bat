@echo off
set "PATH=%PATH%;C:\Users\tomas\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
pdflatex -interaction=nonstopmode test.tex > compile_debug.txt 2>&1
if exist test.pdf echo SUCCESS >> compile_debug.txt
if not exist test.pdf echo FAILURE >> compile_debug.txt
