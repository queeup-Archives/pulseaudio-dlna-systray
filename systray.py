#!/usr/bin/env python

import os
import sys
import gtk

# if you need to add some options to pulseaudio_dlna.py
# please edit this line for your needs.
pulseaudio_dlna = 'pulseaudio-dlna'


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

    # Label Item
    title = gtk.Label()
    title.set_text("<b><span foreground=\"grey\">" + "Pulseaudio DLNA Server:" + "</span></b>")
    title.set_justify(gtk.JUSTIFY_LEFT)
    title.set_alignment(0, 0.5)
    title.set_use_markup(True)
    servicesMenuItem.add(title)
    self.menu.append(servicesMenuItem)

    # Start Item
    self.startMenuItem = gtk.MenuItem('Start')
    self.startMenuItem.connect('activate', self._start)
    self.menu.append(self.startMenuItem)

    # Seperator Item
    self.menu.append(gtk.SeparatorMenuItem())

    # Stop Item
    self.stopMenuItem = gtk.MenuItem('Stop')
    self.stopMenuItem.connect('activate', self._stop)
    # Deactivate Stop Item at the beginning. Cosmetic
    self.stopMenuItem.set_sensitive(False)
    self.menu.append(self.stopMenuItem)

    # Seperator Item
    self.menu.append(gtk.SeparatorMenuItem())

    # Quit Item
    menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    menuItem.connect('activate', self.quit_cb)
    self.menu.append(menuItem)

    self.menu.show_all()

  def _start(self, widget):
    # Activate Stop Item first. Deactivated on beginning.
    self.stopMenuItem.set_sensitive(True)
    # Deactivate Start Item after starting to avoid confuse and start second instant
    self.startMenuItem.set_sensitive(False)
    # execute on backround
    os.system('%s &' % pulseaudio_dlna)

  def _stop(self, widget):
    # Deactivate Stop Item after stoping.
    self.stopMenuItem.set_sensitive(False)
    # Activate Start Item after stoping.
    self.startMenuItem.set_sensitive(True)
    os.system('kill -TERM `pidof pulseaudio-dlna`')

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
