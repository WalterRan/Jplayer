# Jplayer
pip3 install flask prettytable pymysql pynput python-vlc python-xlib sqlalchemy system_hotkey

mkdir /home/pi/Desktop/nfs -p

grep -q '@/home/pi/Jplayer/do' /etc/xdg/lxsession/LXDE-pi/autostart || echo '@/home/pi/Jplayer/do' >> /etc/xdg/lxsession/LXDE-pi/autostart
