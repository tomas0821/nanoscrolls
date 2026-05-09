@echo off
set "PATH=%PATH%;C:\Users\tomas\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
echo PATH SET
echo Running pdflatex version check...
pdflatex --version
echo Running compilation...
pdflatex -interaction=nonstopmode test.tex
echo Done.
