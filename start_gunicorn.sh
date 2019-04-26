cd $WATER_HOME/plant_flask

gunicorn app:app -b 0.0.0.0:5000
