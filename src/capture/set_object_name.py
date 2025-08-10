#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2015 ~suv <suv-sf@users.sf.net>
# Copyright (C) 2010 Alvin Penner
# Copyright (C) 2006 Georg Wiora
# Copyright (C) 2006 Nathan Hurst
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
This extension module can measure arbitrary path and object length
It adds text to the selected path containing the length in a given unit.
Area and Center of Mass calculated using Green's Theorem:
http://mathworld.wolfram.com/GreensTheorem.html
"""

import inkex

from inkex import TextElement, TextPath, Tspan
from inkex.bezier import csparea, cspcofm, csplength
from tkinter import Tk

def log(text):
    with open('C:\\Temp\\log.txt', 'a') as f:
        f.write(str(text) + '\n')

class SetData(inkex.EffectExtension):
    """Measure the length of selected paths"""

    def add_arguments(self, pars):

        pars.add_argument("--type", dest="mtype", default="length",\
            help="Type of measurement")
        pars.add_argument("--method", type=self.arg_method(), default=self.method_textonpath,\
            help="Text Orientation method")
        pars.add_argument("--presetFormat", default="TaP_start", help="Preset text layout")
        pars.add_argument("--startOffset", default="custom", help="Text Offset along Path")
        pars.add_argument("--startOffsetCustom", type=int, default=50,\
            help="Text Offset along Path")
        pars.add_argument("--anchor", default="start", help="Text Anchor")
        pars.add_argument("--position", default="start", help="Text Position")
        pars.add_argument("--angle", type=float, default=0, help="Angle")
        pars.add_argument("-f", "--fontsize", type=int, default=20,\
            help="Size of length label text in px")
        pars.add_argument("-o", "--offset", type=float, default=-6,\
            help="The distance above the curve")
        pars.add_argument("-u", "--unit", default="mm",\
            help="The unit of the measurement")
        pars.add_argument("-p", "--precision", type=int, default=2,\
            help="Number of significant digits after decimal point")
        #pars.add_argument("-s", "--scale", type=float, default=1.1,\
        #    help="Scale Factor (Drawing:Real Length)")

    def get_clipboard(self):
        root = Tk()
        root.withdraw()
        return root.clipboard_get()

    def effect(self):

        if len(self.svg.selection) == 0:
            raise Exception('\n\nNo svg items are selected')

        clip = self.get_clipboard()
        if not clip:
            raise Exception('\n\nNo data in clipboard')

        names = clip.split('|')

        if len(self.svg.selection) != len(names):
            msg = f'\n\nSelection count: {len(self.svg.selection)}\n'
            msg += f'Names count: {len(names)}\n'
            raise Exception('Wall selection / names count mismatch\n' + msg)

        for name, item in zip(clip.split('|'), self.svg.selection):
            item.title = 'origin ' + name

    def method_textonpath(self, node, lenstr):
        return

    def method_presets(self, node, lenstr):
        return

if __name__ == '__main__':
    SetData().run()
