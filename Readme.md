# Setup
1. Install raspbian
2. Deactivate screensaver look [here](https://www.geeks3d.com/hacklab/20160108/how-to-disable-the-blank-screen-on-raspberry-pi-raspbian/)
3. Clone this git repository
4. Put it into autostart. Be carful it might not work with rc.local.
    1. /etc/xdg/lxsession/LXDE-pi/autostart
    2. Add @sh /home/pi/python_photobox_script/start.sh
  

#New
sudo apt-get install python-tk
