from main_app import *

def menuAnimate(self, obj, onmouse):
    # right now minimizing the menu offers no advantage
    # there is no point in having it.
    pass
    # if self.animationDone == True and self.menuPinned == False:
    #     self.anim = QPropertyAnimation(self.ui.sideBar, b'maximumWidth')
    #     self.anim.setStartValue(self.ui.sideBar.width())
    #     if self.ui.sideBar.width() < 100:
    #         self.anim.setEndValue(self.sideBarWidthMax)
    #     else:
    #         self.anim.setEndValue(self.sideBarWidthMin)
    #     self.anim.setEasingCurve(QEasingCurve.InOutCubic)
    #     self.anim.finished.connect(self.animDone)
    #     self.animationDone = False
    #     self.anim.start()
# ------------------------------------------------------------------------

def animDone(self):
    self.animationDone = True
# ------------------------------------------------------------------------
def showWidget(self, obj):
    # check if other widgets are open and close them
    self.anim = QPropertyAnimation(obj, b'geometry')
    if self.anim.state() == self.anim.State.Stopped:
        rect = obj.geometry()
        self.anim.setStartValue(rect)

        # if obj.width() == 0:
        rect.setWidth(1000)
        self.anim.setEndValue(rect)
        self.anim.setDuration(700)
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.anim.start()
# ------------------------------------------------------------------------

def hideWidget(self, obj):
    # check if other widgets are open and close them
    self.anim = QPropertyAnimation(obj, b'geometry')

    self.anim.finished.connect(self.animDone)
    if self.anim.state() == self.anim.State.Stopped:
        rect = obj.geometry()
        self.anim.setStartValue(rect)

        if obj.width() >= 900:
            rect.setWidth(0)
            self.anim.setEndValue(rect)
            self.anim.setDuration(700)
            self.anim.setEasingCurve(QEasingCurve.InOutQuart)
            self.anim.start()