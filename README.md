1. brew --version
if brew not present, run this:
/bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))" 

2. brew install python git
3. brew install --cask cursor
4. Open Cursor.
Install the required Extensions:Python and Jupyter
5. git clone <YOUR_GITHUB_REPO_URL>
6. open folder in cursor

To run project--one time setup to be done:
7. python3 -m venv venv
8. source venv/bin/activate
9. pip install -r requirements.txt
10. paste the service key json file content in bq_module/config/service_key.json

To run notebook:
11. Open main.ipynb (or the guide notebook) in Cursor.
12. Select Kernel (First Time Only):at the top-right of the notebook editor window.
13. Choose Python Environments.
14. Select the one marked ('venv': venv).
