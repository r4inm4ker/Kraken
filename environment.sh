
source "D:/temp/FabricEngine-2.0.0-Windows-x86_64/environment.sh"

KRAKEN_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export KRAKEN_PATH
echo "  Set KRAKEN_PATH=\"$KRAKEN_PATH\""

# FABRIC_EXTS_PATH="$KRAKEN_PATH/Exts;$FABRIC_EXTS_PATH"
# export FABRIC_EXTS_PATH
prepend_env_var FABRIC_EXTS_PATH "$KRAKEN_PATH/Exts"
echo "  Set FABRIC_EXTS_PATH=\"$FABRIC_EXTS_PATH\""

KRAKEN_PATHS=$KRAKEN_PATH/extraComponents
export KRAKEN_PATHS
echo "  Set KRAKEN_PATHS=\"$KRAKEN_PATHS\""

export PYTHONPATH="$KRAKEN_PATH/Python;$PYTHONPATH"
echo "  Set PYTHONPATH=\"$PYTHONPATH\""

prepend_env_var FABRIC_DFG_PATH "$KRAKEN_PATH/CanvasPresets"
echo "  Set FABRIC_DFG_PATH=\"$FABRIC_DFG_PATH\""