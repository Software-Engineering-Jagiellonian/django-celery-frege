if [[ $* == *-v* ]]
then

set -o xtrace

fi

python -m venv ../backend/env
source ../backend/env/Scripts/activate
which python
pip install pip-tools
pip-compile ../backend/requirements.in
pip-sync ../backend/requirements.txt

pre-commit install

cd ../frontend
npm install
cd ../scripts
