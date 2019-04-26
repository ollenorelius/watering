export WATER_HOME="/home/pi/watering"
 
echo $WATER_HOME
cd $WATER_HOME
screen -dmS waterd bash -c "./start_waterd.sh"
screen -dmS seriald bash -c "./start_seriald.sh"
screen -dmS plant_web bash -c "./start_gunicorn.sh"
screen -dmS socketd bash -c "./start_socketd.sh"
