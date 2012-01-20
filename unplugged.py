#!/usr/bin/python

import dbus
import time
import pygst
pygst.require("0.10")
import gst
import gobject
import sys
from dbus.mainloop.glib import DBusGMainLoop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


class MusicControl(object):
    def __init__(self, music_file):
        self.song_path = 'file://%s' % (music_file)
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property('uri', self.song_path)
        self.on_battery = power.Get('/org/freedesktop/UPower', 'OnBattery')
        self.on_low_battery = power.Get('/org/freedesktop/UPower', 'OnLowBattery')

    def play(self):
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.player.set_state(gst.STATE_NULL)

    def update_power_state(self):
        self.on_battery = power.Get('/org/freedesktop/UPower', 'OnBattery')
        self.on_low_battery = power.Get('/org/freedesktop/UPower', 'OnLowBattery')

    def change_state(self):
        self.update_power_state()
        if self.on_battery:
            self.play()

        else:
            self.stop()


if __name__ == '__main__':

    bus = dbus.SystemBus()

    proxy_object = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower')
    power = dbus.Interface(proxy_object, 'org.freedesktop.DBus.Properties')
    music = MusicControl(sys.argv[1])
    bus.add_signal_receiver(music.change_state,
                       dbus_interface="org.freedesktop.UPower",
                       signal_name="Changed")

    gobject.MainLoop().run()
