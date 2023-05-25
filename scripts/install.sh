#check if verbose flag is used
if [[ $* == -v ]]
then
set -o xtrace
fi
set -e

#create and activate virtual enviroment
python -m venv backend/env
source backend/env/Scripts/activate

#install dependencies
pip install pip-tools
pip-compile --output-file backend/requirements.txt backend/requirements.in backend/formatters.in
pip-sync backend/requirements.txt

#install pre-commit hook
pre-commit install

#install npm packages
cd frontend
npm install
cd ..
