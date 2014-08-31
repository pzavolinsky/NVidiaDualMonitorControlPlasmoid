NVidia Dual-Monitor Control Plasmoid
====================================

This is a simple KDE plasmoid to monitor the GPU temperature for NVIDIA cards. Additionally it provides a button to toggle the secondary display in dual monitor setups.

Installation
------------

Go to a terminal window and execute:
```shell
xrandr
```

You should see something like this:
```shell
$ xrandr
Screen 0: minimum 8 x 8, current 1680 x 1050, maximum 8192 x 8192
DVI-I-0 connected primary 1680x1050+0+0 (normal left inverted right x axis y axis) 474mm x 296mm
1680x1050      59.9*+   60.0
1440x900       75.0     59.9
1280x1024      75.0     60.0
1280x960       60.0
1152x864       75.0
1024x768       75.0     60.0
800x600        75.0     60.3     56.2
640x480        75.0     59.9
DVI-I-1 connected (normal left inverted right x axis y axis)
1280x1024      60.0 +   75.0
1152x864       75.0
1024x768       75.0     70.1     60.0
800x600        75.0     72.2     60.3     56.2
640x480        75.0     72.8     59.9
TV-0 disconnected (normal left inverted right x axis y axis)
DVI-I-2 disconnected (normal left inverted right x axis y axis)
DVI-I-3 disconnected (normal left inverted right x axis y axis)
```

Go to `contents/code/main.py` and change the output in both `ENABLE_COMMAND` and `DISABLE_COMMAND` to your secondary output (mine is `DVI-I-1`). You should also change the `--pos` argument there to set the offset of the secondary output. I have `DVI-I-1` to the right of `DVI-I-0` so my offset is 1680x0 (that is offset_x == width of 1st display and offset_y == 0).

In the same terminal, as your normal user (i.e. not root nor sudo) execute:
```shell
   make install
```
 
In KDE right click the desktop and "Add Widget", find a widget named `NVidia-DualMonitor-Control` and drag it to your desktop.

Test
----

If you want to test the plasmoid before installing it run the following command as non-root user:
```shell
make test
```
