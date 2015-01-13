#!/usr/bin/env python

import os
import sys
import gtk

# If pulseaudio_dlna.py not in the same directory please edit this line for your needs
pulseaudio_dlna = sys.path[0] + '/pulseaudio_dlna.py'


class MainClass:

  def __init__(self):
    self.statusIcon = gtk.StatusIcon()
    self.statusIcon.set_from_file(sys.path[0] + '/systray.png')
    self.statusIcon.set_tooltip('Pulseaudio DLNA Server')
    self.statusIcon.set_visible(True)

    self.statusIcon.connect('popup-menu', self.popup_menu_cb)
    self.statusIcon.connect('activate', self.show_menu_cb)

    self.run()

  def run(self):
    self.menu = gtk.Menu()
    servicesMenuItem = gtk.ImageMenuItem()
    
    title = gtk.Label()
    title.set_text("<b><span foreground=\"grey\">" + "Pulseaudio DLNA Server:" + "</span></b>")
    title.set_justify(gtk.JUSTIFY_LEFT)
    title.set_alignment(0, 0.5)
    title.set_use_markup(True)
    servicesMenuItem.add(title)
    self.menu.append(servicesMenuItem)
    startMenuItem = gtk.MenuItem('Start')
    startMenuItem.connect('activate', self._start)
    self.menu.append(startMenuItem)

    self.menu.append(gtk.SeparatorMenuItem())

    stopMenuItem = gtk.MenuItem('Stop')
    stopMenuItem.connect('activate', self._stop)
    self.menu.append(stopMenuItem)

    self.menu.append(gtk.SeparatorMenuItem())

    menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    menuItem.connect('activate', self.quit_cb)
    self.menu.append(menuItem)
    self.menu.show_all()

  def _start(self, widget):
    os.system('pactl load-module module-dbus-protocol')
    os.system('%s &' % pulseaudio_dlna)
  
  def _stop(self, widget):
    os.system('kill -TERM `pidof -x pulseaudio_dlna.py`')

  def quit_cb(self, widget):
    self.statusIcon.set_visible(False)
    gtk.main_quit()
    sys.exit(0)

  def show_menu_cb(self, widget):
    self.menu.popup(None, None, self.menu_pos, 0, gtk.get_current_event_time())

  def popup_menu_cb(self, widget, button, activate_time):
    self.menu.popup(None, None, self.menu_pos, button, activate_time)

  def menu_pos(self, menu):
    return gtk.status_icon_position_menu(self.menu, self.statusIcon)

MainClass()
gtk.main()
