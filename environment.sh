


windows_to_unix_path()
{
  if [[ $1 == *\\* ]]
  then
    echo /"$@" | sed 's/\\/\//g' | sed 's/\://g'
  else
    echo "$@"
  fi
}

windows_split_join_unix_paths()
{
  VAR=$1
  IFS=';' read -ra ARR <<< "$VAR"
  RES=''
  for i in "${ARR[@]}"; do
    RES=$RES":$(windows_to_unix_path $i)"
  done
  echo "$RES"
}

unix_to_windows_path()
{
  echo "$@" | sed 's/^\/\(.\)\//\1:\\/' | sed 's/\//\\/g'
}

friendly_export()
{
  NAME=$1; shift
  VALUE=$1; shift
  eval "export $NAME='$VALUE'"
}

prepend_posix_env_var()
{
  NAME=$1; shift
  VALUE=$1; shift
  eval "QUOTED=\":\$$NAME:\""
  case "$QUOTED" in
    *":$VALUE:"*) :;; # already there
    ::) eval "$NAME='$VALUE'";;
    *) eval "$NAME=\"$VALUE:\$$NAME\"";;
  esac
  eval "NEWVAL=\"\$$NAME\""
  friendly_export "$NAME" "$NEWVAL"
}

prepend_windows_env_var()
{
  NAME=$1; shift
  VALUE=$1; shift
  eval "QUOTED=\";\$$NAME;\""
  case "$QUOTED" in
    *";$VALUE;"*) :;; # already there
    ';;') eval "$NAME='$VALUE'";;
    *) eval "$NAME=\"$VALUE;\$$NAME\"";;
  esac
  eval "NEWVAL=\"\$$NAME\""
  friendly_export "$NAME" "$NEWVAL"
}


set_env_var()
{
  NAME=$1; shift
  VALUE=$1; shift
  if [[ "$OSTYPE" == "msys" ]]; then
    friendly_export "$NAME" "$(unix_to_windows_path $VALUE)"
  else
    friendly_export "$NAME" "$VALUE"
  fi
}

prepend_env_var()
{
  NAME=$1; shift
  VALUE=$1; shift
  if [[ "$OSTYPE" == "msys" ]]; then
    prepend_windows_env_var "$NAME" "$(unix_to_windows_path $VALUE)"
  else
    prepend_posix_env_var "$NAME" "$VALUE"
  fi
}

KRAKEN_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
set_env_var KRAKEN_PATH "$KRAKEN_PATH"
echo "  Set KRAKEN_PATH=\"$KRAKEN_PATH\""


prepend_env_var FABRIC_EXTS_PATH "$KRAKEN_PATH/Exts"
echo "  Set FABRIC_EXTS_PATH=\"$FABRIC_EXTS_PATH\""

friendly_export KRAKEN_PATHS "$KRAKEN_PATH/extraComponents"
echo "  Set KRAKEN_PATHS=\"$KRAKEN_PATHS\""

prepend_env_var PYTHONPATH "$KRAKEN_PATH/Python"
echo "  Set PYTHONPATH=\"$PYTHONPATH\""


prepend_env_var FABRIC_DFG_PATH "$KRAKEN_PATH/Presets/DFG"
echo "  Set FABRIC_DFG_PATH=\"$FABRIC_DFG_PATH\""
