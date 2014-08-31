# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyQt4 import QtCore
import commands
import images_rc
import os

ENABLE_COMMAND  = "xrandr --output DVI-I-1 --pos 1680x0 --auto";
DISABLE_COMMAND = "xrandr --output DVI-I-1 --pos 1680x0 --off";

class NVidiaInfo(plasmascript.Applet):
	
	def __init__(self,parent,args=None):
		plasmascript.Applet.__init__(self,parent)
		self.isDisabled=commands.getoutput("xrandr 2> /dev/null | grep '\*\+' | wc -l") == "1";
		if (os.path.exists("~/.nvinfo")):
			with open("~/.nvinfo", "r") as content_file:
				print "opened"
				if (content_file.read() == "1" and self.isDisabled):
					self.toggle();
	
	def _updateTemperature(self):
		sensor=commands.getoutput("nvidia-settings -q [gpu:0]/GPUCoreTemp | grep gpu:0");
		if sensor.find(".") == -1:
			#Fallback to thermalsensor if GPUCoreTemp is nat available
			sensor=commands.getoutput("nvidia-settings -q [thermalsensor:0]/ThermalSensorReading | grep thermalsensor");
		
		if sensor.find(".") == -1:
			#If nothing works, set a nice message for sensors string to avoid errors
			sensor="): N/A .";
		
		sensor=sensor[sensor.find("):")+2:sensor.rfind(".")+1];
		sensor=sensor.replace(".","");
		
		self.chart.addSample([float(sensor),])
		self.valueLabel.setText(sensor + self.tempunit)
	
	def _updateButton(self):
		text = "Enable"
		img = "disabled"
		if not self.isDisabled:
			text = "Disable"
			img = "enabled"
		self.button.setText(text)
		self.button.setImage(":/images/"+img+".svg")
		
	def init(self):
		self.setHasConfigurationInterface(False)
		self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
		
		theme = Plasma.Theme.defaultTheme()
		textcolor = theme.color(Plasma.Theme.TextColor)
		plotcolor = self.adjustColor(textcolor, 40)
		font = theme.font(Plasma.Theme.DefaultFont)
		
		self.theme = Plasma.Svg(self)
		self.theme.setImagePath("widgets/background")
		
		self.tempunit = unichr(176).encode("latin-1") + 'C'
		self.setBackgroundHints(Plasma.Applet.DefaultBackground)
		
		self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
		
		self.label = Plasma.Label(self.applet)
		
		self.button = Plasma.PushButton(self.applet)
		self.connect(self.button, SIGNAL("clicked()"), self.toggle)
		self.button.setFont(font)
		self.button.setMaximumWidth(100)
		self.button.setStyleSheet("")
		
		self.chart = Plasma.SignalPlotter(self.applet)
		self.chart.setTitle('GPU Temperature')
		self.chart.setVerticalRange(0, 110)
		self.chart.setUseAutoRange(0)
		self.chart.setShowVerticalLines(0)
		self.chart.setShowHorizontalLines(0)
		self.chart.setFontColor(textcolor)
		self.chart.setFont(font)
		self.chart.setShowLabels(0)
		self.chart.setThinFrame(0)
		self.chart.setUnit(self.tempunit)
		self.chart.addPlot(plotcolor)
		self.chart.setSvgBackground('widgets/plot-background')
		self.valueLabel = Plasma.Frame(self.chart)
		self.valueLabel.setFont(font)
		self.chart.setLayout(self.valueLabelLayout(self.valueLabel))
		
		self._updateTemperature();
		self._updateButton();
		
		self.timer = QtCore.QTimer();
		self.timer.setInterval(2000);
		self.timer.start(2000);
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self._updateTemperature)
		
		#self.layout.addItem(self.label)
		#self.layout.addItem(self.button)
		self.layout.addItem(self.chart)
		
		self.buttons = QGraphicsLinearLayout(Qt.Horizontal)
		self.buttons.setMaximumHeight(33)
		self.buttons.addStretch()
		self.buttons.addItem(self.button)
		self.buttons.addStretch()
		self.layout.addItem(self.buttons)
		
		self.applet.setLayout(self.layout)
		
		
	def toggle(self):
		print "notify";
		if self.isDisabled:
			commands.getoutput(ENABLE_COMMAND);
		else:
			commands.getoutput(DISABLE_COMMAND);
		self.isDisabled = not self.isDisabled;
		self._updateButton();
	
	def adjustColor(self, color, percentage):
		(h, s, v, a) = color.getHsvF();
		d = abs(v - 0.5) * (percentage / 100.0);
		if v > 0.5: 
			v -= d
		else:
			v += d;
		
		return QColor.fromHsvF(h, s, v, a);
	
	def valueLabelLayout(self, valueLabel):
		hl = QGraphicsLinearLayout(Qt.Horizontal)
		hl.addStretch()
		hl.addItem(valueLabel)
		hl.addStretch()
		vl = QGraphicsLinearLayout(Qt.Vertical)
		vl.addStretch()
		vl.addItem(hl)
		return vl

def CreateApplet(parent):
	return NVidiaInfo(parent)
