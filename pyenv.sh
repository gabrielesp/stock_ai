#!/bin/bash

# Script for preparing python environment so it is possible to easily execute
# different tests and main entry points.


# ---  F U N C T I O N S  --- #
# --------------------------- #
function pyenv_load {
    if [ $PYENV_STOCK_AI -gt 0 ]; then
        # Already loaded
        echo 'Python environment for StockAI already loaded'
    else
        # Obtain StockAI dir (where this context script is located)
        DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"'/'
        SRCDIR=$DIR'src/'
        
        # Backup PYTHONPATH
        export PYENV_STOCK_AI_PYTHONPATH_BACKUP=$PYTHONPATH
        
        # Update PYTHONPATH so it contains StockAI
        export PYTHONPATH=$PYTHONPATH:${DIR}src

        # Mark StockAI environment as loaded
        export PYENV_STOCK_AI=1
        
        # Message
        echo 'Python environment for StockAI loaded!'
    fi
}

function pyenv_unload {
    if [ $PYENV_STOCK_AI -ne 0 ]; then
        # Restore original PYTHONPATH
        export PYTHONPATH=$PYENV_STOCK_AI_PYTHONPATH_BACKUP
        
        # Forget PYTHONPATH backup, as it is no longer necessary
        unset PYENV_STOCK_AI_PYTHONPATH_BACKUP

        # Mark StockAI environment as unloaded
        export PYENV_STOCK_AI=0

        # Message
        echo 'Python environment for StockAI unloaded!'
    else
        # Already unloaded
        echo 'Python environment for StockAI is not loaded'
    fi
}

# ---  M A I N --- #
# ---------------- #

# Assure PYENV_STOCK_AI is setted to 0 or 1
if [ -z "$PYENV_STOCK_AI" ]; then
    export PYENV_STOCK_AI=0
fi

# Load/unload depending on first arg
if [ "$1" == 'load' ]; then
    # Load
    pyenv_load

elif [ "$1" == 'unload' ]; then
    # Unload
    pyenv_unload

else
    # Usage
cat << EOF
Call this with "load" or "unload" as first argument.
    load -> Load python environment for StockAI
    unload -> Unload python environment for StockAI
EOF

fi
