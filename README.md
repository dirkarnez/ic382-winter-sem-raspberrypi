ic382-winter-sem-raspberrypi
============================
```bash
cd ~/development/agv_base_control

source devel/setup.bash && rosrun controller controller.py

catkin_make && source devel/setup.bash &&  sudo chmod 777 /dev/ttyUSB0 && roslaunch robot_encoder_odom agv_base_control_odom.launch
```
