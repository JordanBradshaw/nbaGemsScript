# nbaGemsScript
NBA Game Log Generator

# How to setup
python -m ensurepip --upgrade

python -m venv ./.venv

. .\.venv\Scripts\Activate
# (.venv) PS C:\?\?\nbaGemsScript> You should see (.venv)

pip install wheel yahoo_fantasy_api pandas nba_api

## To run the script
# Windows
. .\.venv\Scripts\Activate
python nbaGemsScript.py
# Linux
. ./.venv/Scripts/Activate
python nbaGemsScript.py
