"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD & Mickael GARCIA - Toonkit
    Copyright (C) 2014-2022 Toonkit
    http://toonkit-studio.com/

    Toonkit Module Lite is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Toonkit Module Lite is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Toonkit Module Lite.  If not, see <http://www.gnu.org/licenses/>
-------------------------------------------------------------------------------
"""

from qtpy import QtCore, QtWidgets

# Slider that accept float values, Use "decimals" arg to set precision value
class QFloatSlider(QtWidgets.QSlider):
    """
        The QFloatSlider is a simple Slider who accepts and send float values.
    """
    def __init__(self, orientation = QtCore.Qt.Horizontal, decimals = 3):
        """
            Constructor of QFloatSlider.

            :param orientation: The oritentation of the slider. Horizontal by default.
            :param deciamls: The maximum number of decimals that can be given by the slider. 3 by default.

            :type orientation: QtCore.Qt.Orientation
            :type decimals: int
        """
        super(QFloatSlider, self).__init__(orientation)

        self.decimals = decimals
    
    def setMaximum(self, maximum):
        super(QFloatSlider, self).setMaximum(maximum*10**self.decimals)
    
    def setMinimum(self, minimum):
        super(QFloatSlider, self).setMinimum(minimum*10**self.decimals)

    def setRange(self, min, max):
        super(QFloatSlider, self).setRange(min*10**self.decimals, max*10**self.decimals)
    
    def value(self):
        return (super (QFloatSlider, self).value())*10**(self.decimals*-1)

    def setValue(self, value):
        super(QFloatSlider, self).setValue(round(value*10**self.decimals, self.decimals))

    def maximum(self):
        return super(QFloatSlider, self).maximum()*(10**(self.decimals*-1))
    
    def minimum(self):
        return super(QFloatSlider, self).minimum()*(10**(self.decimals*-1))
        
# FloatEdit that accept math operation, with grabe to change value
class QFloatEdit(QtWidgets.QLineEdit):
    """
    The QFloatEdit is a one line textedit which accepts only float values and math operations.

    :ivar clicked: initial value: False
    :ivar mousePos: inital value: 0
    
    """
    mouseMoved = QtCore.Signal(float)
    mousePressed = QtCore.Signal()
    mouseReleased = QtCore.Signal()
    windowActivate = QtCore.Signal()
    windowDesactivate = QtCore.Signal()

    def __init__(self, value = 0.0, decimals = 3, min = -10000, max = 10000):
        """
            :param value: default value of the component. 0.0 by default.
            :param decimals: Set the maximum number of decimals that can be given by the slider. 3 by default.
            :param min: Set the minimum value that can be displayed in the component. -10000 by default.
            :param max: Set the maximum value that can be displayed in the component. 10000 by default.

            :type value: float
            :type decumals: int
            :type min: float
            :type max: float
        """
        super(QFloatEdit, self).__init__(str(value))
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.setDragEnabled(True)
        self.clicked = False
        self.mousePos = 0
        self.oldPose = 0
        self.decimals = int(decimals)
        self.min = min
        self.max = max
    
    def setText(self, value):
        """
            This method set the line edit's text. The value is truncated to min and max value.

            :param value: Value to set.

            :type value: float
        """
        if value >= self.max:
            value = self.max
        elif value <= self.min:
            value = self.min
        super(QFloatEdit, self).setText(str(round(value, self.decimals)))

    def changePose(self, event, multiplyer):
        if event.x() > self.oldPose:
            self.mousePos =1* 10**(multiplyer)
        elif event.x()< self.oldPose:
            self.mousePos = -1* 10**(multiplyer)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            self.windowActivate.emit()
        elif event.type()== QtCore.QEvent.WindowDeactivate:
            self.windowDesactivate.emit()
        return False

    def mouseMoveEvent(self, event, *args, **kwargs): 
        # method called when the mouse over and move in the element. If clicked and modifyerKey pressed, offset the current value.
        super(QFloatEdit, self).mouseMoveEvent(event, *args, **kwargs)
        if self.clicked:
            modifier = QtWidgets.QApplication.keyboardModifiers()
            if modifier == QtCore.Qt.NoModifier:
                pass
            elif modifier == QtCore.Qt.ControlModifier: # Ctrl key pressed
                self.changePose(event, -2)
            elif modifier == QtCore.Qt.ShiftModifier:# Shift key pressed
                self.changePose(event, -1)
            elif (modifier & QtCore.Qt.ControlModifier) and (modifier & QtCore.Qt.ShiftModifier): # Ctrl and Shift key pressed
                self.changePose(event, -0)

            if (modifier & QtCore.Qt.ControlModifier) or (modifier & QtCore.Qt.ShiftModifier): # Ctrl or Shift key pressed
                value = eval(self.text()) + self.mousePos
                self.setText(value)
                self.mouseMoved.emit(self.mousePos)
            self.oldPose = event.x()

    def mousePressEvent(self, event):
        super(QFloatEdit, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked = True
        else:
            self.clicked = False
        self.mousePressed.emit()

    def mouseReleaseEvent(self, event):
        self.clicked = False
        self.oldPose = 0
        self.mousePos = 0
        self.mouseReleased.emit()

# SpinGroup with Label, Float edit and float slider
class QSpinBoxGrp(QtWidgets.QHBoxLayout):
    """
        The QSpinBoxGrp is a groupe component with multiple elements: a QLabel, a QFloatEdit and a QFloatSider connected.
        This component cans store multiple values, edite thems and displayed the last one.

        :ivar eventMute: Mute the class's event to avoid recursive calls.
        :ivar values: List of multiple values.
    """
    valueChanged = QtCore.Signal(list)
    mousePressed = QtCore.Signal()
    mouseReleased = QtCore.Signal()
    mouseMoved = QtCore.Signal()
    editingStarted = QtCore.Signal()
    editingFinished = QtCore.Signal(list)

    def __init__(self, parent=None, label = None, value=0.0, uiMax = 10, max = 10000, uiMin = -10, min = -10000, decimals = 3):
        """
            :param parent: Parent of the component. None by deflaut.
            :param label: Label displayed at the left of the component. None by default.
            :param value: Default value setted to the component. 0.0 by default.
            :param uiMax: Displayed maximum value of the slider component. 10 by default.
            :param max: True maximum value can be displayed and setted to the component. 10000 by default
            :param uiMin: Displayed minimum value of the slider component. -10 by default.
            :param min: True minimum value can be displayed and setted to the component. -10000 by default
            :param decimals: The maximum number of decimals that can be given by the slider. 3 by default.

            :type parent: QtCore.QtWidgets.QWidget
            :type label: str
            :type value: float
            :type uiMax: float
            :type max: float
            :type uiMin: float
            :type min: float
            :type deciamls: int
        """
        super(QSpinBoxGrp, self).__init__()
        self.installEventFilter(self)
        # Statics:
        self.eventMute = False
        self.mouseClicked = False

        # Property:
        self.max = max
        self.min = min
        self.uiMax = uiMax
        self.uiMin = uiMin
        self.values = [0.0]
        self.decimals = int(decimals)
        
        # UI:
        parent.addLayout(self)
        self.label = QtWidgets.QLabel(label)
        self.text = QFloatEdit(value, self.decimals, self.min, self.max)
        self.slider = QFloatSlider()
        self.slider.setRange(self.uiMin, self.uiMax)
        
        self.addWidget(self.label)
        self.addWidget(self.text)
        self.addWidget(self.slider)
        self.setStretch(2,1)

        def _connectSlider():
            if not self.eventMute:
                if self.mouseClicked == False:
                    self.mouseClicked = True
                    self.editingStarted.emit()
                self.eventMute = True
                try:
                    value = float(self.text.text())
                    if value >= self.uiMax:
                        self._extendSlider(value)
                    elif value <= self.uiMin:
                        self._reduceSlider(value)
                    self._offsetValues(value)
                    self.updateUI()
                    self.valueChanged.emit(self.values)
                except:pass
                self.eventMute = False

        def _connectLigneEdit():
            if not self.eventMute:
                if self.mouseClicked == False:
                    self.mouseClicked = True
                    self.editingStarted.emit()
                self.eventMute = True
                value = self.slider.value()
                self._offsetValues(value)
                self.updateUI()
                self.eventMute = False

        # Connections :
        self.text.mousePressed.connect(self._mousePressed) # Emit mousePressed Event on text pressed
        self.slider.sliderPressed.connect(self._mousePressed) # Emit mousePressed Event on slider pressed
        self.text.mouseReleased.connect(self._mouseReleased) # Emit mouseReleased Event on text released
        self.slider.sliderReleased.connect(self._mouseReleased) # Emit mouseRelesed Event on slider released
        self.slider.valueChanged.connect(self._valueChanged) # Emit valueChanged on slider valueChanged
        self.text.mouseMoved.connect(_connectSlider) # Connect Text to Slider
        self.slider.valueChanged.connect(_connectLigneEdit) # Connect Slider to text
        self.text.returnPressed.connect(self.returnPressedValue)
        self.text.editingFinished.connect(self.validatedValue)
        
    def returnPressedValue(self):
        value = self.text.text()
        if not self.eventMute:
            try:
                self.editingStarted.emit()
                self.valueChanged.emit(self.values)
                newValue = eval(value)
                self.eventMute = True
                self.setValue(newValue)
                self.eventMute = False
                self._editingFinished()
            except:
                try:
                    newValues = []
                    for x in self.values:
                        newVal = eval("x" + value.replace("=", ""))
                        newValues.append(newVal)
                    self.editingStarted.emit()
                    self.valueChanged.emit(self.values)
                    self.eventMute = True
                    self.values = newValues
                    self.updateUI()
                    self.eventMute = False
                    self._editingFinished()
                except:
                    newValue = self.values[-1]
                    self.editingStarted.emit()
                    self.valueChanged.emit(self.values)
                    self.eventMute = True
                    self.setValue(newValue)
                    self._editingFinished()
                    self.eventMute = False

    def validatedValue(self):
        value = self.text.text()
        if not self.eventMute:
            try:
                self.editingStarted.emit()
                self.valueChanged.emit(self.values)
                newValue = eval(value)
                self.eventMute = True
                self.setValue(newValue, True)
                self.eventMute = False
                self._editingFinished()
            except:
                try:
                    newValues = []
                    for x in self.values:
                        newVal = eval("x" + value.replace("=", ""))
                        newValues.append(newVal)
                    self.editingStarted.emit()
                    self.valueChanged.emit(self.values)
                    self.eventMute = True
                    self.values = newValues
                    self.updateUI()
                    self.eventMute = False
                    self._editingFinished()
                except:
                    newValue = self.values[-1]
                    self.editingStarted.emit()
                    self.valueChanged.emit(self.values)
                    self.eventMute = True
                    self.setValue(newValue, True)
                    self._editingFinished()
                    self.eventMute = False

    def setMaximum(self, max):
        self.max = max
        if self.slider.value() > self.max:
            self.slider.setValue(self.max)
        self.slider.setMaximum(self.max)

    def setMinimum(self, min):
        self.min = min
        if self.slider.value() < self.min:
            self.slider.setValue(self.min)
        self.slider.setMinimum(self.min)

    def setUiMax(self, uiMax):
        self.uiMax = uiMax
        self.slider.setMaximum(self.uiMax)
    
    def setUiMin(self, uiMin):
        self.uiMin = uiMin
        self.slider.setMinimum(self.uiMin)

    def setValue(self, value, offset=False):
        """
            Thus funciont set the value of the component and edit the attribut values with or without offset.
            
            :param value: Value to set to the component
            :param offset: Set if the value will be offceted or not.

            :type value: float
            :type offset: bool
        """
        self.eventMute = True
        if not offset:
            self._updateValues(value)
        elif offset:
            self._offsetValues(value)
        self.text.setText(value)
        self.slider.setValue(value)
        self.eventMute = False
        self.updateUI()
        
    def updateUI(self):
        if self.values[-1] >= self.uiMax:
            self._extendSlider(self.values[-1])
        elif self.values[-1] <= self.uiMin:
            self._reduceSlider(self.values[-1])
        self.eventMute = True
        self.slider.setValue(self.values[-1])
        self.text.setText(self.values[-1])
        self.eventMute = False
            
        return False

    def _mousePressed(self):
        self.mousePressed.emit()
    
    def _mouseReleased(self):
        if self.mouseClicked == True:
            self.mouseClicked = False
            self._editingFinished()
        self.mouseReleased.emit()
    
    def _offsetValues(self, value): # CBB : renvoyer le calcule plutot qu'une valeur a ajouter !
        toAddValue = value - self.values[-1]
        for index in range(len(self.values)):
            self.values[index] = self.values[index] + toAddValue
    
    def _updateValues(self, value):
        for index in range(len(self.values)):
            self.values[index] = value

    def _valueChanged(self):
        value = self.slider.value()
        self._offsetValues(value)
        if not self.eventMute:
            self.valueChanged.emit(self.values)

    def _editingFinished(self):
        if not self.eventMute:
            self.editingFinished.emit(self.values)

    def _extendSlider(self, value):
        if value < self.max:
            while value > self.slider.maximum():
                newMax = self.slider.maximum()*2
                if newMax > self.max:
                    self.slider.setMaximum(self.max)
                    self.uiMax = self.max
                else:
                    self.slider.setMaximum(newMax)
                    self.uiMax = newMax
        else:
            self.slider.setMaximum(self.uiMax)

    def _reduceSlider(self, value):
        if value > self.min:
            while value < self.slider.minimum():
                newMin = self.slider.minimum()*2
                if newMin < self.min:
                    self.slider.setMinimum(self.min)
                    self.uiMin = self.min
                else:
                    self.slider.setMinimum(newMin)
                    self.uiMin = newMin
        else:
            self.slider.setMinimum(self.min)