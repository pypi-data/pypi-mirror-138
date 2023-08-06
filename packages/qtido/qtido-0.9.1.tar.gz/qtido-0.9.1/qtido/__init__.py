
import sys as _sys
import queue as _queue
import inspect as _inspect
from functools import wraps as _wraps
# ^ important: end with a from (not a plain import) to avoid the minifier to merge with the import numpy (that should remain in the try)

try:
    import numpy as _np
    _np_numbers = [_np.int32, _np.int64, _np.float32, _np.float64]
except:
    _np_numbers = []

try:
    from PyQt4 import QtGui, QtCore
    Application = QtGui.QApplication
    Widget = QtGui
except:
    from PyQt5 import QtGui, QtCore, QtWidgets
    Application = QtWidgets.QApplication
    Widget = QtWidgets

def share(f):
    f.shared = True
    return f

def _window(v):
    return isinstance(v, Fenetre)
_window.__checkname__ = 'Fenetre'

def _turtle(v):
    return isinstance(v, Tortue)
_turtle.__checkname__ = 'Tortue'

def _pointlist(v):  # for 2d points
    try:
        for l in v:
            for e in l:
                if type(e) not in [int, float] + _np_numbers:
                    return False
            if len(l) != 2:
                return False
        return True
    except:
        return False
_pointlist.__checkname__ = 'liste de points'

def num(v):
    return type(v) in [int, float] + _np_numbers
num.__checkname__ = 'int/float'

def num01(v):
    return type(v) in [int, float] + _np_numbers and 0 <= v <= 1
num01.__checkname__ = 'interval [0, 1]'

def check(*types):
    def deco(f):
        argspec = _inspect.getargspec(f)
        defaults = [] if argspec.defaults is None else argspec.defaults
        arg_names = argspec.args

        @_wraps(f)
        def sub(*args, **kwargs):
            toadd = len(types) - len(args)
            if len(defaults) >= toadd:
                added = args + tuple(defaults[-toadd:])
            else:
                added = args
            for i,t in enumerate(types):
                if len(added) <= i < len(added) + len(defaults):
                    print('ERREUR : dans « {fname} », le paramètre n°{i1} (nommé « {pname} ») est manquant.\n'.format(fname=f.__name__, i=i, i1=i+1, pname=arg_names[i], arg_names=arg_names, args=args))
                    continue
                exp = None
                if _inspect.isfunction(t):
                    if not t(added[i]):
                        exp = t.__checkname__
                else:
                    if type(added[i]) != t:
                        exp = t.__name__
                if exp is not None:
                    print('ERREUR : dans « {fname} », le paramètres n°{i1} n′a pas le type attendu « {expected} » mais le type « {ptype} » (valeur « {pval} »).\n'.format(fname=f.__name__, i=i, i1=i+1, pname=arg_names[i], pval=added[i], ptype=type(added[i]), arg_names=arg_names, args=args, expected=exp))
            return f(*args, **kwargs)
        return sub
    return deco


def painter(fill):
    def painter__(f):
        @_wraps(f)
        def sub(self, *args, **kwargs):
            paint = QtGui.QPainter()
            paint.begin(self.backbuffer)
            paint.setRenderHint(QtGui.QPainter.Antialiasing)
            paint.translate(0.5, 0.5) # as 0,0 means the first pixel for us
            if self.transform is not None:
                tx, ty, sx, sy, r = self.transform
                paint.translate(tx, ty)
                paint.scale(sx, sy)
                paint.rotate(r)
            self.p = paint
            if fill:
                self.pen = QtCore.Qt.NoPen #QtGui.QPen(self.color, 0.0001)
                self.brush = self.color
                paint.setPen(self.pen)
                paint.setBrush(self.brush)
            else:
                self.pen = QtGui.QPen(self.color, self.strokeWidth)
                paint.setPen(self.pen)
            f(self, *args, **kwargs)
            paint.end()
            self.p = None
            self.pen = None
            self.brush = None
            if self.interactive:
                self.re_afficher()
        sub.shared = True
        return sub
    return painter__

class Tortue:
    def __init__(self, f):
        self.f = f
        self.x = self.f.w / 2
        self.y = self.f.h / 2
        self.a = 0
        self.down = True
        self.f.effacer()

    typed = lambda *args: check(_turtle, *args)

    @share
    @typed(num)
    def tortue_gauche(self, da):
        self.a -= da
    @share
    @typed(num)
    def tortue_droite(self, da):
        self.a += da
    @share
    @typed()
    def tortue_stop(self):
        self.down = False
    @share
    @typed()
    def tortue_trace(self):
        self.down = True
    @share
    @typed(num)
    def tortue_avance(self, d):
        import math
        _x = self.x
        _y = self.y
        self.x += d * math.cos(math.radians(self.a))
        self.y += d * math.sin(math.radians(self.a))
        if self.down:
            self.f.ligne(_x, _y, self.x, self.y)


#################
class Fenetre:
    def __init__(self, w, h, interactive, parent=None):
        self.w = w
        self.h = h
        self.interactive = interactive
        self.widget = Widget.QWidget(parent)
        self.widget.setFixedSize(w, h)
        self.widgets = {}
        self.closed = _queue.Queue()
        self.shown = _queue.Queue()
        self.hasBeenClosed = False
        self.hasBeenShown = False
        self.pressedKeys = set()
        self.events = _queue.Queue()
        self.previousWait = None
        self.nextFiringInstant = None
        self.backbuffer = QtGui.QPixmap(w, h)
        def paintEvent(event):
            if not self.hasBeenShown:
                self.shown.put("Shown")
                self.hasBeenShown = True
            paint = QtGui.QPainter(self.widget)
            paint.drawPixmap(0, 0, self.backbuffer)
        def closeEvent(event):
            self.closed.put("Closed")
            self.hasBeenClosed = True
            event.accept() #event.ignore()
        def keyPressEvent(event):
            self.events.put(event.key())
            self.pressedKeys.add(event.key())
        def keyReleaseEvent(event):
            if event.key() in self.pressedKeys:
                self.pressedKeys.remove(event.key())
                self.events.put(-event.key())
        def mousePressEvent(event):
            self.events.put(("PRESS", event.x(), event.y(), event.button()))
        def mouseMoveEvent(event):
            self.events.put(("MOVE", event.x(), event.y()))
        def mouseReleaseEvent(event):
            self.events.put(("RELEASE", event.x(), event.y(), event.button()))
        self.widget.paintEvent = paintEvent
        self.widget.closeEvent = closeEvent
        self.widget.keyPressEvent = keyPressEvent
        self.widget.keyReleaseEvent = keyReleaseEvent
        self.widget.mousePressEvent = mousePressEvent
        self.widget.mouseMoveEvent = mouseMoveEvent
        self.widget.mouseReleaseEvent = mouseReleaseEvent
        self.widget.show()
        self.faitShowing()
        self.couleur(1, 1, 1)
        self.epaisseur_du_trait(1)
        self.annuler_transformation()
        self.effacer()

    typed = lambda *args: check(_window, *args)

    def registerWidget(self, name, widget):
        if name in self.widgets:
            print("warning-key-already-used: {}".format(name))
        self.widgets[name] = widget

    @share
    @typed()
    def re_afficher(self):
        self.widget.repaint()
        QtCore.QCoreApplication.processEvents()

    @painter(True)
    @typed()
    def effacer(self):
        self.p.setBrush(QtGui.QColor(0,0,0))
        self.p.drawRect(-1, -1, self.w+2, self.h+2)
        self.annuler_transformation()

    @share
    @typed(num01, num01, num01, num01)
    def couleur(self, r, g, b, a=1):
        self.color = QtGui.QColor(0,0,0)
        self.color.setRgbF(r, g, b, a)

    @share
    @typed(num)
    def epaisseur_du_trait(self, w):
        self.strokeWidth = w

    @share
    @typed()
    def annuler_transformation(self):
        self.transform = None

    @share
    @typed(num, num, num, num, num)
    def utiliser_transformation(self, tx, ty, sx=1, sy=1, r=0):
        self.transform = (tx, ty, sx, sy, r)

    @painter(False)
    @typed(num, num, num)
    def cercle(self, cx, cy, r):
        self.p.drawEllipse(QtCore.QRectF(cx-r, cy-r, 2*r, 2*r))

    @painter(True)
    @typed(num, num, num)
    def disque(self, cx, cy, r):
        self.p.drawEllipse(QtCore.QRectF(cx-r, cy-r, 2*r, 2*r))

    @painter(False)
    @typed(num, num, num, num)
    def ligne(self, x1, y1, x2, y2):
        self.p.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))

    @painter(False)
    @typed(num, num, num, num)
    def cadre(self, x1, y1, x2, y2):
        self.p.drawRect(QtCore.QRectF(x1, y1, x2-x1-1, y2-y1-1)) # -1 to keep the "rectangle" behavior

    @painter(True)
    @typed(num, num, num, num)
    def rectangle(self, x1, y1, x2, y2):
        self.p.translate(-0.5, -0.5) # undo as it seems necessary for anti-aliasing alignment
        self.p.drawRect(QtCore.QRectF(x1, y1, x2-x1, y2-y1))

    @painter(False)
    @typed(_pointlist, bool)
    def polyligne(self, points, ferme=True):
        if len(points) <= 1: return
        path = QtGui.QPainterPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        if ferme:
            path.lineTo(points[0][0], points[0][1])
        self.p.strokePath(path, self.pen)

    @painter(True)
    @typed(_pointlist, bool)
    def polygone(self, points, ferme=True):
        if len(points) <= 1: return
        path = QtGui.QPainterPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        if ferme:
            path.lineTo(points[0][0], points[0][1])
        self.p.fillPath(path, self.brush)

    @painter(True)
    @share
    def grille_numpy(self, tab, pas, taille, gauche, top, couleur='-green +red'):
        W = tab.shape[1]
        H = tab.shape[0]
        tab = _np.clip(tab, 0, 1)
        alpha = 1
        if type(couleur) != type(lambda a:a):
            inds = {'red': 0, 'rouge':0, 'green': 1, 'vert': 1, 'blue': 2, 'bleu': 2}
            a = [0, 0, 0]
            b = [0, 0, 0]
            for part in couleur.split(' '):
                i = inds[part[1:]]
                if part[0] == '+': a[i] = 1
                if part[0] == '-': a[i], b[i] = -1, 1
                if part[0] == '1': b[i] = 1
                if part[0] == '½': b[i] = 0.5
            couleur = lambda v: [a[0]*v+b[0], a[1]*v+b[1], a[2]*v+b[2]]
            
        self.p.translate(-0.5, -0.5) # undo as it seems necessary for anti-aliasing alignment
        col = QtGui.QColor(0,0,0)
        for i in range(W):
            for j in range(H):
                v = tab[j,i]
                col.setRgbF(*couleur(v))
                self.p.setBrush(col)
                x = gauche + i*pas
                y = top + j*pas
                t = taille-1
                self.p.drawRect(x-t/2, y-t/2, t, t) # -1 to keep the "rectangle" behavior


    @painter(False)
    @typed(num, num, num, str)
    def texte(self, gauche, bas, taille, txt):
        s = taille
        self.p.setFont(QtGui.QFont('Arial', s))
        BIG = 10000
        self.p.drawText(QtCore.QRectF(gauche, bas-BIG/2-s/2, BIG, BIG), QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, txt)

    @painter(False)
    @typed(num, num, num, str)
    def texte_centre(self, gauche, bas, taille, txt):
        s = taille
        self.p.setFont(QtGui.QFont('Arial', s))
        BIG = 10000
        self.p.drawText(QtCore.QRectF(gauche-BIG/2, bas-BIG/2-s/2, BIG, BIG), QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, txt)

    @share
    @typed()
    def faitShowing(self):
        import time
        while True: # block until we get the event
            QtCore.QCoreApplication.processEvents()
            try:
                what = self.shown.get(True, .05)
                self.shown.put(what) # put it back in case faitShowing gets called again
                break
            except:
                pass # loop
    @share
    @typed()
    def attendre_fermeture(self):
        import time
        self.re_afficher()
        while True: # block until we get the event
            QtCore.QCoreApplication.processEvents()
            try:
                what = self.closed.get(True, .05)
                self.closed.put(what) # put it back in case attendre_fermeture gets called again
                break
            except:
                pass # loop
    @share
    @typed(num)
    def attendre_pendant(self, ms):
        import time
        now = time.time()
        nextFire = now + ms * 0.001
        self.re_afficher()
        while nextFire - now > 0:
            QtCore.QCoreApplication.processEvents()
            time.sleep(min(.01, nextFire - now))
            now = time.time()
    @share
    @typed(bool)
    def reinitialiser_attendre_evenement(self, trigger=False):
        import time
        now = time.time()
        if trigger:
            self.previousWait = now
            self.nextFiringInstant = self.previousWait
        else:
            self.previousWait = now
            self.nextFiringInstant = None
    @share
    @typed(num)
    def attendre_evenement(self, ms):
        import time
        now = time.time()
        if self.previousWait is None: # very first call or after a clear
            self.previousWait = now - ms*0.001
        if self.nextFiringInstant is None: # this is not a continuation call (after an event)
            self.nextFiringInstant = self.previousWait + ms*0.001
            self.previousWait += ms*0.001
        self.re_afficher()
        # python lock and Qt don't play well, so we do pseudo active wait
        def eventOrNull(secondsToWait):
            try:
                return self.events.get(True, secondsToWait)
            except:
                return None
        self.lastEvent = None
        while self.nextFiringInstant - now > 0:
            QtCore.QCoreApplication.processEvents()
            self.lastEvent = eventOrNull(min(.01, self.nextFiringInstant - now))
            if not self.lastEvent is None:
                return
            now = time.time()
        self.nextFiringInstant = None
        return
    @share
    @typed()
    def dernier_evenement(self):
        return self.lastEvent
    @share
    def est_souris(self, e, types = ["PRESS", "RELEASE", "MOVE"]):
        if type(types) == str:
            types = [types]
        return type(e) == tuple and e[0] in types
    @share
    def coordonnees_souris(self, e):
        if est_souris(self, e):
            _,x,y,b = e
            return [x,y]
        else:
            return None
    @share
    @typed()
    def les_touches_appuyees(self):
        return list(self.pressedKeys)
    @share
    @typed()
    def est_fermee(self):
        QtCore.QCoreApplication.processEvents()
        return self.hasBeenClosed
    @share
    @typed()
    def fermer_fenetre(self):
        QtCore.QCoreApplication.processEvents()
        return self.widget.close()
    @share
    @typed(str, num, num, num, num, str)
    def ajouter_bouton(self, eventName, x1, y1, x2, y2, caption):
        self.widget.hide()
        button = Widget.QPushButton(caption, self.widget)
        button.clicked.connect(lambda: self.events.put(eventName))
        button.setGeometry(x1, y1, x2-x1, y2-y1)
        self.registerWidget(eventName, button)
        self.widget.show()
    @share
    @typed(str, num, num, num, num)
    def ajouter_champ_texte(self, eventName, x1, y1, x2, y2):
        self.widget.hide()
        lineEdit = Widget.QLineEdit("", self.widget)
        lineEdit.textChanged.connect(lambda: self.events.put(eventName))
        lineEdit.setGeometry(x1, y1, x2-x1, y2-y1)
        self.registerWidget(eventName, lineEdit)
        self.widget.show()
    @share
    @typed(str)
    def lire_champ_texte(self, eventName):
        return self.widgets[eventName].text()
    @share
    @typed(str, str)
    def changer_champ_texte(self, eventName, value):
        return self.widgets[eventName].setText(value)
    @share
    @typed(str, num, num, num, num)
    def ajouter_zone_texte(self, eventName, x1, y1, x2, y2):
        self.widget.hide()
        lineEdit = Widget.QTextEdit("", self.widget)
        lineEdit.textChanged.connect(lambda: self.events.put(eventName))
        lineEdit.setGeometry(x1, y1, x2-x1, y2-y1)
        self.registerWidget(eventName, lineEdit)
        self.widget.show()
    @share
    @typed(str)
    def lire_zone_texte(self, eventName):
        return self.widgets[eventName].toPlainText()
    @share
    @typed(str, str)
    def changer_zone_texte(self, eventName, value):
        return self.widgets[eventName].setPlainText(value)
    @share
    @typed(str, num, num, num, num, num, num)
    def ajouter_slider(self, eventName, x1, y1, x2, y2, vMin=0, vMax=999):
        self.widget.hide()
        slider = Widget.QSlider(QtCore.Qt.Horizontal, self.widget)
        slider.valueChanged.connect(lambda: self.events.put(eventName))
        slider.setRange(vMin, vMax)
        slider.setGeometry(x1, y1, x2-x1, y2-y1)
        self.registerWidget(eventName, slider)
        self.widget.show()
    @share
    @typed(str)
    def lire_slider(self, eventName):
        return self.widgets[eventName].value()
    @share
    @typed(str, int)
    def changer_slider(self, eventName, value):
        return self.widgets[eventName].setValue(value)
    @share
    @typed()
    def supprime_widgets(self):
        for k in self.widgets:
            self.widgets[k].setParent(None)
        self.widgets = {}
    @share
    @typed(str)
    def exporter_image(self, nom_de_fichier):
        out = QtGui.QPixmap(self.w, self.h)
        paint = QtGui.QPainter()
        paint.begin(out)
        #paint.setRenderHint(QtGui.QPainter.Antialiasing)
        bg = QtGui.QColor(0,0,255).darker()
        fr = QtGui.QColor(255,255,255)
        tx = QtGui.QColor(255,255,255)
        paint.drawPixmap(0, 0, self.backbuffer)
        paint.setBrush(bg)
        paint.drawRect(0,0, 250, 30)
        paint.setBrush(QtCore.Qt.NoBrush)
        BIG = 10000
        s = 10
        try:
            bbg = QtGui.QColor(bg)
            bbg.setBlue(bbg.blue()+2)
            paint.setPen(QtGui.QPen(bbg, 1))
            paint.setFont(QtGui.QFont('Arial', s))
            import getpass
            import datetime
            now = datetime.datetime.now()
            what = getpass.getuser() + " " + now.isoformat()
            ts = 7
            font = QtGui.QFont('', ts)
            font.setStyleHint(QtGui.QFont.SansSerif, QtGui.QFont.NoAntialias)
            paint.setFont(font)
            paint.drawText(5, 8-BIG/2-ts/2, BIG, BIG, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, what)
            paint.setPen(QtGui.QPen(fr, 1))
        except e:
            print("Partial-error-while-saving-file '{}'".format(nom_de_fichier))
        paint.setPen(QtGui.QPen(fr, 1))
        paint.drawRect(0,0, 250, 30)
        font = QtGui.QFont('monospace', s)
        font.setStyleHint(QtGui.QFont.SansSerif, QtGui.QFont.NoAntialias)
        paint.setFont(font)
        paint.drawText(10, 20-BIG/2-s/2, BIG, BIG, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, "Fichier : "+nom_de_fichier)
        if not out.save(nom_de_fichier):
            print("Erreur de sauvegarde du fichier '{}'".format(nom_de_fichier))
        paint.end()

# function to create a new window
@check(int, int, bool)
def creer(w, h, interactive=False):
    return Fenetre(w, h, interactive)
@check(_window)
def creer_tortue(f):
    return Tortue(f)

# register all "@shared" methods as functions
for m in dir(Fenetre):
    meth = getattr(Fenetre, m)
    if hasattr(meth, "shared"):
        locals()[m] = meth
for m in dir(Tortue):
    meth = getattr(Tortue, m)
    if hasattr(meth, "shared"):
        locals()[m] = meth

app = Application(_sys.argv)
# was trying to solve pb with spyder
#app.moveToThread(QtCore.QThread())
#QtCore.pyqtRemoveInputHook()
#app.exec_()
