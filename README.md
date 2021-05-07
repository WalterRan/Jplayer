# sparrow_player
pip3 install flask prettytable pymysql pynput python-vlc python-xlib sqlalchemy system_hotkey

mkdir /home/pi/Desktop/nfs -p

grep -q '@/home/pi/sparrow_player/do' /etc/xdg/lxsession/LXDE-pi/autostart || echo '@/home/pi/sparrow_player/do' >> /etc/xdg/lxsession/LXDE-pi/autostart

# Run in CentOS
yum install kernel-headers-$(uname -r) -y
yum install gcc -y
yum install python-devel -y
yum install python3-pip -y
yum install python3-devel -y

pip3 install python-vlc pynput flask python-xlib system_hotkey prettytable pymysql sqlalchemy alembic

yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y
yum install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm -y
yum info vlc
yum install vlc -y

sed -i 's/geteuid/getppid/' /usr/bin/vlc
