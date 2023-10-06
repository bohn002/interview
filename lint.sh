echo "Running pylint"
pylint chopper.py
echo "Running flake8"
flake8 --count chopper.py