:: nmeset foo zero, ukitakakurollback iset iwe 1 for safety
echo off

set foo=0
echo %foo%

if %foo%==1 goto roll

pause
exit

:roll
echo "It will rollback"
python "C:\Program Files\Google\google_appengine\appcfg.py" rollback "C:\Users\CharlesMagoti\Desktop\myvastev2"
pause
