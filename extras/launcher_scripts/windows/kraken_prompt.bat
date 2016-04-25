@ECHO OFF
ECHO "Releasing The Kraken!"

call D:\fabric\FabricEngine-2.1.0-Windows-x86_64\environment.bat

set KRAKEN_PATH=D:\dev\kraken
set FABRIC_EXTS_PATH=%FABRIC_EXTS_PATH%;%KRAKEN_PATH%\Exts;
set FABRIC_DFG_PATH=%FABRIC_DFG_PATH%;%KRAKEN_PATH%\Presets\DFG;
set PYTHONPATH=%PYTHONPATH%;%KRAKEN_PATH%\Python;

cd /d %KRAKEN_PATH%

call cmd