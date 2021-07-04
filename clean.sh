rm sparrow_player.egg-info -rf
rm build -rf
rm ChangeLog -rf
rm dist -rf
# rm .tox -rf
rm list -rf

find . -type d -name '__pycache__' | xargs rm -rf
find . -name '*.pyc' | xargs rm -rf

umount /home/pi/Desktop/nfs

tree
