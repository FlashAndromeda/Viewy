# Viewy
Very simple and minimalistic image viewer.

Used through the 'Send to' part of the context menu. Right-click the image to exit\
Add a .cmd file to your shell:sendto folder with the following code (ofc substitute SCRIPT_PATH with the path to the script lol):

@echo off \
cls \
python SCRIPT_PATH %1

\
\
\
I can probably simplify the code a fair bit and add some functionality but I'm lazy rn, maybe in the future.