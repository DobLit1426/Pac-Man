from intern.zeichenfenster import *



## Wrapperklasse zur Beschreibung von Objekten des Typs Dreieck

class Dreieck:



    ## Die Initalisierungsmethode sorgt für die Anfangsbelegung der Attribute für Position und Aussehen.

    # @param x anfängliche x-Position der Spitze (Standardwert: 60)

    # @param y anfängliche y-Position der Spitze (Standardwert: 10)

    # @param winkel anfänglicher Winkel (Standardwert: 0)

    # @param breite anfängliche Breite des Objekts der Klasse Dreieck (Standardwert: 100)

    # @param hoehe anfängliche Höhe des Objekts der Klasse Dreieck (Standardwert: 100)

    # @param farbe anfängliche Farbe des Objekts der Klasse Dreieck (Standardwert: "rot")

    # @param sichtbar anfängliche Sichtbarkeit (Standardwert: True)       

    def __init__(self, x = 60, y = 10, winkel = 0, breite = 100, hoehe = 100, farbe = "rot", sichtbar = True):

        ## x-Position der Spitze

        self.x = x

        ## y-Position der Spitze 

        self.y = y

        ## Winkel

        self.winkel = winkel

        ## Breite des Dreiecks

        self.breite = breite

        ## Höhe des Dreiecks

        self.hoehe = hoehe

        ## Farbe des Dreiecks

        self.farbe = farbe

        ## Sichtbarkeit des Dreiecks (True oder False)

        self.sichtbar = sichtbar

        ## Referenz auf das Dreieckssymbol

        self.symbol = DreieckIntern(self.farbe, self.x, self.y, self.breite, self.hoehe, self.winkel, self.sichtbar)



    ## Setzt die Position (der Spitze) des Dreiecks.

    # @param x x-Position der Spitze

    # @param y y-Position der Spitze

    def PositionSetzen(self, x, y):

        self.x = x

        self.y = y

        self.symbol.PositionSetzen(self.x - self.breite/2, self.y)

    

    ## Verschiebt das Dreieck um die angegebenen Werte.

    # @param deltaX Verschiebung in x-Richtung

    # @param deltaY Verschiebung in y-Richtung

    def Verschieben(self, deltaX, deltaY):

        self.x += deltaX

        self.y += deltaY

        self.symbol.PositionSetzen(self.x - self.breite/2, self.y)

     

    ## Dreht das Dreieck.

    # @param grad Drehwinkel (mathematisch positiver Drehsinn) im Gradmass

    def Drehen(self, grad):

        self.winkel = (self.winkel+grad)%360

        self.symbol.WinkelSetzen(self.winkel)

        

    ## Setzt den Drehwinkel des Dreiecks.

    # Die Winkelangabe ist in Grad,positive Werte drehen gegen den Uhrzeigersinn, negative Werte drehen im Uhrzeigersinn (mathematisch positiver Drehsinn).

    # @param winkel der (neue) Drehwinkel des Dreiecks

    def WinkelSetzen(self, winkel):

        self.winkel = winkel%360

        self.symbol.WinkelSetzen(self.winkel)

     

    ## Setzt die Größe des Dreiecks.

    # @param breite (neue) Breite

    # @param hoehe (neue) Höhe

    def GroesseSetzen (self, breite, hoehe):

        self.breite = breite

        self.hoehe = hoehe

        self.symbol.GroesseSetzen(self.breite, self.hoehe)  

        self.symbol.PositionSetzen(self.x - self.breite/2, self.y)

    

    ## Setzt die Farbe des Dreiecks.

    # Erlaubte Farben sind:

    # "weiß", "weiss", "rot", "grün", "gruen", "blau", "gelb", "magenta", "cyan", "hellgelb", "hellgrün", "hellgruen","orange", "braun", "grau", "schwarz", "transparent"

    # Au&szlig;erdem sind rgb-Farbwerte erlaubt in der Form (r, g, b), die Zahlen jeweils aus dem Bereich 0.255 

    # @param farbe (neue) Farbe

    def FarbeSetzen(self, farbe):

        self.farbe = farbe

        self.symbol.FarbeSetzen(self.farbe)

    

    ## Schaltet die Sichtbarkeit des Dreiecks ein oder aus.

    # Erlaubte Parameterwerte: true, false

    # @param sichtbar (neue) Sichtbarkeit des Dreiecks  

    def SichtbarkeitSetzen(self, sichtbar):

        self.sichtbar = sichtbar

        self.symbol.SichtbarkeitSetzen(self.sichtbar)



    ## Entfernt das Dreieck aus dem Zeichenfenster.

    def Entfernen(self):

        self.symbol.Entfernen()

        del self

    

    ## Bringt das Dreieck eine Ebene nach vorn.

    def NachVorneBringen(self):

        self.symbol.NachVorneBringen()

    

    ## Bringt das Dreieck in die vorderste Ebene.

    def GanzNachVornBringen(self):

        self.symbol.GanzNachVornBringen()

    

    ## Bringt das Dreieck eine Ebene nach hinten.

    def NachHintenBringen(self):

        self.symbol.NachHintenBringen()

    

    ## Bringt das Dreieck in die hinterste Ebene.

    def GanzNachHintenBringen(self):

        self.symbol.GanzNachHintenBringen()







## Klasse zur Beschreibung der Ereignisbehandlung (Taktimpulse, Mausklicks, Tastaturereignisse, die vom Zeichenfenster registriert wurden)

class Ereignisbehandlung:



    ## Der Konstruktor meldet das Objekt als Beobachter beim Zeichenfenster an.

    def __init__(self):

        Zeichenfenster().BeobachterRegistrieren(self)



    ## Aktionsmethode, die bei jedem Taktschlag ausgeführt wird.

    #  Muss bei Bedarf von einer Unterklasse überschrieben werden.

    def AktionAusfuehren(self):

        #print("Tick")

        pass

    

    ## Aktionsmethode, die bei jedem Tastendruck ausgelöst wird.

    #  Muss bei Bedarf von einer Unterklasse überschrieben werden.

    # @param taste gedrückte Taste

    def TasteGedrueckt(self, taste):

        print("Taste gedrückt: ", taste)



    ## Aktionsmethode, die bei jedem Mausklick ausgelöst wird.

    #  Muss bei Bedarf von einer Unterklasse überschrieben werden.

    # @param button Maustaste (1-links, 2-Mausrad, 3-rechts, 4-Mausrad nach oben, 5-Mausrad nach unten)

    # @param pos Position des Mausklicks

    def MausGeklickt(self, button, pos):

        print("Maustaste: ", button, " an Position: ", pos)

    

    ## Methode zum Starten des Takgebers   

    def Starten(self):

        Zeichenfenster().Starten()



    ## Methode zum Stoppen des Takgebers      

    def Anhalten(self):

        Zeichenfenster().Stoppen()



    ## Methode zum Setzen der Geschwindigkeit

    # @param fps frames per second - Bilder pro Sekunde

    def GeschwindigkeitSetzen(self, fps):

        Zeichenfenster().GeschwindigkeitSetzen(fps)

        

    ## Das gesamte Fenster wird neu gezeichnet.

    # Dies passiert nach einem Durchlauf der Hauptroutine des Programms automatisch.

    # Will man innerhalb einer Methode ein Neuzeichnen veranlassen (z. B. um nach Bewegung eines Objekts auf Berührung zu testen), so kann diese Methode ein Neuzeichnen zu anderer Zeit bewirken.

    def FensterNeuZeichnen():

        Zeichenfenster().FensterNeuZeichnen()

        

        

## Wrapperklasse zur Beschreibung der Figur

class Figur:



    ## Die Initalisierungsmethode sorgt für die Anfangsbelegung der Attribute für Position und Aussehen.

    # @param x anfängliche x-Position der Mitte der Figur (Standardwert: 100)

    # @param y anfängliche y-Position der Mitte der Figur (Standardwert: 200)

    # @param winkel anfänglicher Winkel (Standardwert: 0)

    # @param groesse anfängliche Größe des Objekts der Klasse Figur (Standardwert: 40)

    # @param sichtbar anfängliche Sichtbarkeit  (Standardwert: True)

    def __init__(self, x = 100, y = 200, winkel = 0, groesse = 40, sichtbar = True):

        ## x-Position der Figurenmitte

        self.x = x

        ## y-Position der Figurenmitte      

        self.y = y

        ## Drehwinkel (0<=winkel<=360)

        self.winkel = winkel

        ## Größe der quadratischen Figur

        self.groesse = groesse

        ## Sichtbarkeit der Figur (True oder False)

        self.sichtbar = sichtbar

        ## Referenz auf das Symbol

        self.symbol = FigurIntern(self.x, self.y, self.groesse, self.winkel, self.sichtbar)

        Zeichenfenster().BeobachterRegistrieren(self)



    ## Aktionsmethode, die bei jedem Taktschlag ausgeführt wird.

    #  Muss bei Bedarf in einer Unterklasse überschrieben werden.

    def AktionAusfuehren(self):

        pass



    ## Aktionsmethode, die bei jedem Tastendruck ausgelöst wird.

    #  Muss bei Bedarf in einer Unterklasse überschrieben werden.

    # @param taste gedrückte Taste    

    def TasteGedrueckt(self, taste):

        pass

     

    ## Aktionsmethode, die bei jedem Mausklick ausgelöst wird.

    #  Muss bei Bedarf in einer Unterklasse überschrieben werden.

    # @param button Maustaste (1-links, 2-Mausrad, 3-rechts, 4-Mausrad nach oben, 5-Mausrad nach unten)

    # @param pos Position des Mausklicks

    def MausGeklickt(self, button, pos):

        pass

    

    ## Setzt die Position der Figur.

    # @param x x-Position der Mitte der Figur

    # @param y y-Position der Mitte der Figur

    def PositionSetzen(self, x, y):

        self.x = x

        self.y = y

        self.symbol.PositionSetzen(self.x, self.y)



    ## Verschiebt die Figur in die Richtung ihres Winkels.

    # @param laenge Anzahl der Längeneinheiten                  

    def Gehen(self,laenge):

        self.symbol.Gehen(laenge)

        self.x = self.symbol.x

        self.y = self.symbol.y

 

    ## Dreht die Figur

    # @param grad Drehwinkel (mathematisch positiver Drehsinn) im Gradmass       

    def Drehen(self, grad):

        self.winkel = (self.winkel+grad)%360

        self.symbol.WinkelSetzen(self.winkel)



    ## Setzt den Drehwinkel der Figur.

    # Die Winkelangabe ist in Grad, positive Werte drehen gegen den Uhrzeigersinn, negative Werte drehen im Uhrzeigersinn (mathematisch positiver Drehsinn). 0°: rechts; 90°: oben; 180°: links; 270° unten

    # @param winkel der (neue) Drehwinkel der Figur              

    def WinkelSetzen(self, winkel):

        self.winkel = winkel%360

        self.symbol.WinkelSetzen(self.winkel)



    ## Setzt die Größe der Figur.

    # @param groesse Größe des umgebenden Quadrats  

    def GroesseSetzen (self, groesse):

        self.groesse = groesse

        self.symbol.GroesseSetzen(groesse)  



    ## Schaltet die Sichtbarkeit der Figur ein oder aus.

    # Erlaubte Parameterwerte: true, false

    # @param sichtbar (neue) Sichtbarkeit der Figur

    def SichtbarkeitSetzen(self, sichtbar):

        self.sichtbar = sichtbar

        self.symbol.SichtbarkeitSetzen(self.sichtbar)



    ## Entfernt die Figur aus dem Zeichenfenster.

    def Entfernen(self):

        self.symbol.Entfernen()

        Zeichenfenster().BeobachterEntfernen(self)

        del self

      

    ## Bringt die Figur eine Ebene nach vorn.   

    def NachVorneBringen(self):

        self.symbol.NachVorneBringen()

        

    ## Bringt die Figur in die vorderste Ebene.

    def GanzNachVornBringen(self):

        self.symbol.GanzNachVornBringen()

    

    ## Bringt die Figur eine Ebene nach hinten.

    def NachHintenBringen(self):

        self.symbol.NachHintenBringen()

    

    ## Bringt die Figur in die hinterste Ebene.   

    def GanzNachHintenBringen(self):

        self.symbol.GanzNachHintenBringen()

     

    ## Bringt die Figur zu ihrem Startpunkt.   

    def ZumStartpunktGehen(self):

        self.symbol.ZumStartpunktGehen()

        self.x = self.symbol.x

        self.y = self.symbol.y

        self.winkel = self.symbol.winkel

     

    ## Liefert den Winkel der Figur.

    # @return Winkel

    def WinkelGeben(self):

        return self.winkel



    ## Liefert die x-Position der Figur.

    # @return x-Position  

    def XPositionGeben(self):

        return self.x



    ## Liefert die y-Position der Figur.

    # @return y-Position      

    def YPositionGeben(self):

        return self.y

    

    ## Testet, ob die Figur eine Grafik-Figur berührt.

    # @return true, wenn die Figur und eine Grafikfigur überlappen

    def Beruehrt(self):

        return self.symbol.Beruehrt()



    ## Testet, ob die Figur eine Objekt berührt, das die gegebene Farbe enthält.

    # (die Farbe muss nicht unbedingt sichtbar oder direkt berührt werden)

    # @param farbe Farbe, auf die getestet werden soll.

    # @return true wenn ein Objekt mit der Farbe berührt wird.    

    def BeruehrtFarbe(self, farbe):

        return self.symbol.BeruehrtFarbe(farbe)



    ## Testet, ob die Figur eine Objekt berührt.

    # @param objekt Objekt, mit dem eine Überschneidung geprüft werden soll.

    # @return true wenn das übergebene Objekt mit der Farbe berührt.        

    def BeruehrtObjekt(self, objekt):

        return self.symbol.BeruehrtObjekt(objekt)



    ## Erzeugt ein neues, rechteckiges Element einer eigenen Darstellung der Figur.

    # Alle Werte beziehen sich auf eine Figur der Größe 100x100 und den Koordinaten (0|0) in der Mitte des Quadrats

    # @param x x-Wert der linken oberen Ecke des Rechtecks innerhalb der Figur (-50<=x<=50)

    # @param y y-Wert der linken oberen Ecke des Rechtecks innerhalb der Figur (-50<=y<=50)

    # @param breite Breite des Rechtecks innerhalb der Figur (0<=breite<=50-x)

    # @param hoehe Höhe des Rechtecks innerhalb der Figur (0<=hoehe<=50-x)

    # @param farbe Farbe des Figurelements

    def FigurteilFestlegenRechteck(self, x, y, breite, hoehe, farbe):

        self.symbol.FigurteilFestlegenRechteck(x,y,breite, hoehe, farbe)



    ## Erzeugt ein neues, elliptisches Element einer eigenen Darstellung der Figur.

    # Alle Werte beziehen sich auf eine Figur der Größe 100x100 und den Koordinaten (0|0) in der Mitte des Quadrats

    # @param x x-Wert der linken oberen Ecke des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (-50<=x<=50)

    # @param y y-Wert der linken oberen Ecke des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (-50<=y<=50)

    # @param breite Breite des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (0<=breite<=50-x)

    # @param hoehe Höhe des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (0<=hoehe<=50-x)

    # @param farbe Farbe des Figurelements        

    def FigurteilFestlegenEllipse(self, x, y, breite, hoehe, farbe):

        self.symbol.FigurteilFestlegenEllipse(x,y,breite, hoehe, farbe)



    ## Erzeugt ein neues, dreieckiges Element einer eigenen Darstellung der Figur.

    # Die Werte müssen passend zur Größe der Figur gewählt werden (Standardwert: 40) 

    # @param x1 x-Wert des ersten Punktes innerhalb der Figur (-50<=x1<=50)

    # @param y1 y-Wert des ersten Punktes innerhalb der Figur (-50<=y1<=50)

    # @param x2 x-Wert des zweiten Punktes innerhalb der Figur (-50<=x2<=50)

    # @param y2 y-Wert des zweiten Punktes innerhalb der Figur (-50<=y2<=50)

    # @param x3 x-Wert des dritten Punktes innerhalb der Figur (-50<=x3<=50)

    # @param y3 y-Wert des dritten Punktes innerhalb der Figur (-50<=y3<=50)

    # @param farbe Farbe des Figurelements     

    def FigurteilFestlegenDreieck(self, x1, y1 ,x2, y2, x3, y3, farbe):

        self.symbol.FigurteilFestlegenDreieck(x1, y1 ,x2, y2, x3, y3, farbe)



    ## Setzt die Figur wieder auf die Standarddarstellung zurück

    def EigeneFigurLoeschen(self):

        self.symbol.StandardfigurErzeugen()

    

    ## Stellt das Symbol neu dar.    

    def Darstellen(self):

        self.symbol.Darstellen()

        

    ## Das gesamte Fenster wird neu gezeichnet.

    # Dies passiert nach einem Durchlauf der Hauptroutine des Programms automatisch.

    # Will man innerhalb einer Methode ein Neuzeichnen veranlassen (z. B. um nach Bewegung eines Objekts auf Berührung zu testen), so kann diese Methode ein Neuzeichnen zu anderer Zeit bewirken.

    def FensterNeuZeichnen():

        self.symbol.FensterNeuZeichnen()



## Wrapperklasse zur Beschreibung von Objekten der Klasse Kreis

class Kreis:



    ## Die Initalisierungsmethode sorgt für die Anfangsbelegung der Attribute für Position und Aussehen.

    # @param x anfängliche x-Position des Mittelpunkts (Standardwert: 60)

    # @param y anfängliche y-Position des Mittelpunkts (Standardwert: 60)

    # @param radius anfänglicher Radius des Kreises (Standardwert: 50)

    # @param winkel anfänglicher Winkel (Standardwert: 0)

    # @param farbe anfängliche Farbe Kreises (Standardwert: "rot")

    # @param sichtbar anfängliche Sichtbarkeit (Standardwert: True)      

    def __init__(self, x = 60, y = 60, radius = 50, winkel = 0, farbe = "rot", sichtbar = True):

        ## x-Position des Mittelpunkts

        self.x = x

        ## y-Position des Mittelpunkts

        self.y = y

        ## Radius des Kreises       

        self.radius = radius

        ## Drehwinkel (0<=winkel<=360)

        self.winkel = winkel

        ## Farbe des Kreises

        self.farbe = farbe

        ## Sichtbarkeit des Kreises (True oder False)

        self.sichtbar = sichtbar

        ## Referenz auf das Rechteckssymbol

        self.symbol = KreisIntern(self.farbe, self.x, self.y, self.radius, self.winkel, self.sichtbar)



    ## Setzt die Position des Mittelpunktes.

    # @param x x-Position des Mittelpunkts

    # @param y y-Position des Mittelpunkts

    def PositionSetzen(self, x, y):

        self.x = x

        self.y = y

        self.symbol.PositionSetzen(self.x-self.radius, self.y-self.radius)



    ## Verschiebt den Kreis um die angegebenen Werte.

    # @param deltaX Verschiebung in x-Richtung

    # @param deltaY Verschiebung in y-Richtung        

    def Verschieben(self, deltaX, deltaY):

        self.x += deltaX

        self.y += deltaY

        self.symbol.PositionSetzen(self.x-self.radius, self.y-self.radius)



    ## Dreht den Kreis.

    # @param grad Drehwinkel (mathematisch positiver Drehsinn) im Gradmass

    def Drehen(self, grad):

        self.winkel = (self.winkel+grad)%360

        self.symbol.WinkelSetzen(self.winkel)



    ## Setzt den Drehwinkel des Kreises.

    # Die Winkelangabe ist in Grad,positive Werte drehen gegen den Uhrzeigersinn, negative Werte drehen im Uhrzeigersinn (mathematisch positiver Drehsinn).

    # @param winkel der (neue) Drehwinkel des Kreises          

    def WinkelSetzen(self, winkel):

        self.winkel = winkel%360

        self.symbol.WinkelSetzen(self.winkel)



    ## Setzt den Radius des Kreises.

    # @param radius (neuer) Radius

    def RadiusSetzen (self, radius):

        self.radius = radius

        self.symbol.GroesseSetzen(self.radius * 2, self.radius * 2)

        self.symbol.PositionSetzen(self.x - radius, self.y - radius)



    ## Setzt die Farbe des Kreises.

    # Erlaubte Farben sind:

    # "weiss", "weiss", "rot", "grün", "gruen", "blau", "gelb", "magenta", "cyan", "hellgelb", "hellgrün", "hellgruen","orange", "braun", "grau", "schwarz", "transparent"

    # Au&szlig;erdem sind rgb-Farbwerte erlaubt in der Form (r, g, b), die Zahlen jeweils aus dem Bereich 0.255 

    # @param farbe (neue) Farbe         

    def FarbeSetzen(self, farbe):

        self.farbe = farbe

        self.symbol.FarbeSetzen(self.farbe)



    ## Schaltet die Sichtbarkeit des Kreises ein oder aus.

    # Erlaubte Parameterwerte: true, false

    # @param sichtbar (neue) Sichtbarkeit des Kreises        

    def SichtbarkeitSetzen(self, sichtbar):

        self.sichtbar = sichtbar

        self.symbol.SichtbarkeitSetzen(self.sichtbar)



    ## Entfernt den Kreis aus dem Zeichenfenster.

    def Entfernen(self):

        self.symbol.Entfernen()

        del self



    ## Bringt den Kreis eine Ebene nach vorn.       

    def NachVorneBringen(self):

        self.symbol.NachVorneBringen()



    ## Bringt den Kreis in die vorderste Ebene.    

    def GanzNachVornBringen(self):

        self.symbol.GanzNachVornBringen()



    ## Bringt den Kreis eine Ebene nach hinten.    

    def NachHintenBringen(self):

        self.symbol.NachHintenBringen()



    ## Bringt den Kreis in die hinterste Ebene.      

    def GanzNachHintenBringen(self):

        self.symbol.GanzNachHintenBringen()

        





## Wrapperklasse zur Beschreibung von Objekten der Klasse Rechteck

class Rechteck:



    ## Die Initalisierungsmethode sorgt für die Anfangsbelegung der Attribute für Position und Aussehen.

    # @param x anfängliche x-Position der linken oberen Ecke (Standardwert: 10)

    # @param y anfängliche y-Position der linken oberen Ecke (Standardwert: 10)

    # @param winkel anfänglicher Winkel (Standardwert: 0)

    # @param breite anfängliche Breite (Standardwert: 100)

    # @param hoehe anfängliche Höhe (Standardwert: 200)

    # @param farbe anfängliche Farbe (Standardwert: "rot")

    # @param sichtbar anfängliche Sichtbarkeit (Standardwert: True)

    def __init__(self, x = 10, y = 10, winkel = 0, breite = 100, hoehe = 200, farbe = "rot", sichtbar = True):

        ## x-Position der linken oberen Ecke

        self.x = x

        ## y-Position der linken oberen Ecke

        self.y = y

        ## Drehwinkel (0<=winkel<=360)

        self.winkel = winkel

        ## Breite des Rechteck

        self.breite = breite

        ## Höhe des Rechtecks

        self.hoehe = hoehe

        ## Farbe des Rechtecks

        self.farbe = farbe

        ## Sichtbarkeit des Rechtecks (True oder False)

        self.sichtbar = sichtbar  

        ## Referenz auf das Rechteckssymbol

        self.symbol = RechteckIntern(self.farbe, self.x, self.y, self.breite, self.hoehe, self.winkel, self.sichtbar)        



    ## Setzt die Position der linken oberen Ecke des Rechtecks.

    # @param x x-Position der Spitze

    # @param y y-Position der Spitze

    def PositionSetzen(self, x, y):

        self.x = x

        self.y = y

        self.symbol.PositionSetzen(self.x, self.y)

     

    ## Verschiebt das Rechteck um die angegebenen Werte.

    # @param deltaX Verschiebung in x-Richtung

    # @param deltaY Verschiebung in y-Richtung

    def Verschieben(self, deltaX, deltaY):

        self.x += deltaX

        self.y += deltaY

        self.symbol.PositionSetzen(self.x, self.y)

     

    ## Dreht das Rechteck.

    # @param grad Drehwinkel (mathematisch positiver Drehsinn) im Gradmass

    def Drehen(self, grad):

        self.winkel = (self.winkel+grad)%360

        self.symbol.WinkelSetzen(self.winkel)



    ## Setzt den Drehwinkel des Rechtecks.

    # Die Winkelangabe ist in Grad,positive Werte drehen gegen den Uhrzeigersinn, negative Werte drehen im Uhrzeigersinn (mathematisch positiver Drehsinn).

    # @param winkel der (neue) Drehwinkel des Rechtecks      

    def WinkelSetzen(self, winkel):

        self.winkel = winkel%360

        self.symbol.WinkelSetzen(self.winkel)

    

    ## Setzt die Größe des Rechtecks.

    # @param breite (neue) Breite

    # @param hoehe (neue) Höhe

    def GroesseSetzen (self, breite, hoehe):

        self.breite = breite

        self.hoehe = hoehe

        self.symbol.GroesseSetzen(self.breite, self.hoehe)       

    

    ## Setzt die Farbe des Rechtecks.

    # Erlaubte Farben sind:

    # "weiß", "weiss", "rot", "grün", "gruen", "blau", "gelb", "magenta", "cyan", "hellgelb", "hellgrün", "hellgruen","orange", "braun", "grau", "schwarz", "transparent"

    # Au&szlig;erdem sind rgb-Farbwerte erlaubt in der Form (r, g, b), die Zahlen jeweils aus dem Bereich 0.255 

    # @param farbe (neue) Farbe    

    def FarbeSetzen(self, farbe):

        self.farbe = farbe

        self.symbol.FarbeSetzen(self.farbe)

     

    ## Schaltet die Sichtbarkeit des Rechtecks ein oder aus.

    # Erlaubte Parameterwerte: true, false

    # @param sichtbar (neue) Sichtbarkeit des Rechtecks

    def SichtbarkeitSetzen(self, sichtbar):

        self.sichtbar = sichtbar

        self.symbol.SichtbarkeitSetzen(self.sichtbar)



    ## Entfernt das Rechteck aus dem Zeichenfenster.

    def Entfernen(self):

        self.symbol.Entfernen()

        del self

   

    ## Bringt das Rechteck eine Ebene nach vorn.   

    def NachVorneBringen(self):

        self.symbol.NachVorneBringen()

    

    ## Bringt das Rechteck in die vorderste Ebene.

    def GanzNachVornBringen(self):

        self.symbol.GanzNachVornBringen()

       

    ## Bringt das Rechteck eine Ebene nach hinten.

    def NachHintenBringen(self):

        self.symbol.NachHintenBringen()

    

    ## Bringt das Rechteck in die hinterste Ebene.   

    def GanzNachHintenBringen(self):

        self.symbol.GanzNachHintenBringen()

        



## Wrapperklasse zur Beschreibung eines Textes

class Text:



    ## Die Initalisierungsmethode sorgt für die Anfangsbelegung der Attribute für Position und Aussehen.

    # @param x anfängliche x-Position der linken oberen Ecke des Textfeldes (Standardwert: 10)

    # @param y anfängliche y-Position der linken oberen Ecke des Textfeldes (Standardwert: 10)

    # @param winkel anfänglicher Winkel (Standardwert: 0)

    # @param textgroesse anfängliche Textgröße (Standardwert: 12)

    # @param farbe anfängliche Schriftfarbe  (Standardwert: "schwarz")

    # @param sichtbar anfängliche Sichtbarkeit (Standardwert: True)      

    def __init__(self, x = 10, y = 10, winkel = 0, textgroesse = 12, farbe = "schwarz", sichtbar = True):

        ## x-Position der linken oberen Ecke

        self.x = x

        ## y-Position der linken oberen Ecke

        self.y = y

        ## Drehwinkel (0<=winkel<=360)

        self.winkel = winkel

        ## Schriftgroesse

        self.textgroesse = textgroesse

        ## Farbe des Textes

        self.farbe = farbe

        ## Sichtbarkeit des Textes (True oder False)

        self.sichtbar = sichtbar

        ## Referenz auf das Symbol

        self.symbol = TextIntern(self.farbe, self.x, self.y, self.textgroesse, self.winkel, self.sichtbar)



    ## Setzt die Position der linken oberen Ecke des Textes.

    # @param x x-Position der Spitze

    # @param y y-Position der Spitze

    def PositionSetzen(self, x, y):

        self.x = x

        self.y = y

        self.symbol.PositionSetzen(self.x, self.y)



    ## Legt den dargestellten Text fest.

    # @param text dargestellter Text        

    def TextSetzen(self, text):

        self.symbol.TextSetzen(text)

 

    ## Legt die Schriftgröße fest.

    # @param groesse Schriftgröße        

    def TextGroesseSetzen(self, groesse):

        self.textgroesse = groesse

        self.symbol.TextGroesseSetzen(groesse)

    

    ## Erhöht die Schriftgröße        

    def TextVergroessern(self):

        self.symbol.TextVergroessern()

        self.textgroesse = self.symbol.groesse



    ## Verkleinert die Schriftgröße          

    def TextVerkleinern(self):

        self.symbol.TextVergroessern()

        self.textgroesse = self.symbol.groesse



    ## Verschiebt die Schrift.

    # @param deltaX Verschiebung in x-Richtung  

    # @param deltaY Verschiebung in y-Richtung  

    def Verschieben(self, deltaX, deltaY):

        self.x += deltaX

        self.y += deltaY

        self.symbol.PositionSetzen(self.x, self.y)



    ## Dreht das Textfeld.

    # @param grad Drehwinkel (mathematisch positiver Drehsinn) im Gradmass        

    def Drehen(self, grad):

        self.winkel = (self.winkel+grad)%360

        self.symbol.WinkelSetzen(self.winkel)



    ## Setzt den Drehwinkel des Textfeldes.

    # Die Winkelangabe ist in Grad,positive Werte drehen gegen den Uhrzeigersinn, negative Werte drehen im Uhrzeigersinn (mathematisch positiver Drehsinn).

    # @param winkel der (neue) Drehwinkel des Textfeldes         

    def WinkelSetzen(self, winkel):

        self.winkel = winkel%360

        self.symbol.WinkelSetzen(self.winkel)



    ## Legt die Größe des Textfeldes fest.

    # @param breite Breite des Textfeldes

    # @param hoehe Höhe des Textfeldes 

    def GroesseSetzen (self, breite, hoehe):

        self.breite = breite

        self.hoehe = hoehe

        self.symbol.GroesseSetzen(self.breite, self.hoehe)       



    ## Setzt die Farbe des Textes.

    # Erlaubte Farben sind:

    # "weiß", "weiss", "rot", "grün", "gruen", "blau", "gelb", "magenta", "cyan", "hellgelb", "hellgrün", "hellgruen","orange", "braun", "grau", "schwarz", "transparent"

    # Au&szlig;erdem sind rgb-Farbwerte erlaubt in der Form (r, g, b), die Zahlen jeweils aus dem Bereich 0.255 

    # @param farbe (neue) Farbe         

    def FarbeSetzen(self, farbe):

        self.farbe = farbe

        self.symbol.FarbeSetzen(self.farbe)



    ## Schaltet die Sichtbarkeit des Textes ein oder aus.

    # Erlaubte Parameterwerte: true, false

    # @param sichtbar (neue) Sichtbarkeit des Texts       

    def SichtbarkeitSetzen(self, sichtbar):

        self.sichtbar = sichtbar

        self.symbol.SichtbarkeitSetzen(self.sichtbar)



    ## Entfernt den Text aus dem Zeichenfenster.

    def Entfernen(self):

        self.symbol.Entfernen()

        del self



    ## Bringt den Text eine Ebene nach vorn.         

    def NachVorneBringen(self):

        self.symbol.NachVorneBringen()



    ## Bringt den Text in die vorderste Ebene    

    def GanzNachVornBringen(self):

        self.symbol.GanzNachVornBringen()



    ## Bringt den Text eine Ebene nach hinten.    

    def NachHintenBringen(self):

        self.symbol.NachHintenBringen()



    ## Bringt den Text in die hinterste Ebene.    

    def GanzNachHintenBringen(self):

        self.symbol.GanzNachHintenBringen()

        



## Wrapperklasse zur Beschreibung der Turtle

class Turtle:



    ## Die Initalisierungsmethode sorgt für die Anfangsbelegung der Attribute für Position und Aussehen.

    # @param x anfängliche x-Position der Schwanzspitze (Standardwert: 100)

    # @param y anfängliche y-Position der Schwanzspitze (Standardwert: 200)

    # @param winkel anfänglicher Winkel (Standardwert: 0)

    # @param farbe anfängliche Farbe des Objekts (Standardwert: "schwarz")

    # @param sichtbar anfängliche Sichtbarkeit (Standardwert: True)

    # @param stiftUnten gibt an, ob der Stift unten ist (Zeichenmodus) (Standardwert: True)   

    def __init__(self, x = 100, y = 200, winkel = 0, farbe = "schwarz", sichtbar = True, stiftUnten = True):

        ## x-Position der Schwanzspitze

        self.x = x

        ## y-Position der Schwanzspitze

        self.y = y

        ## Drehwinkel (0<=winkel<=360)

        self.winkel = winkel

        ## Stiftfarbe der Turtle (auch Augen- und Schwanzfarbe)       

        self.farbe = farbe

        ## Größe der Turtle      

        self.groesse = 40

        ## Sichtbarkeit der Turtle (True oder False)

        self.sichtbar = sichtbar

         ## Gibt an, ob die Turtle im Zeichenmodus oder ob der Stift angehoben ist.      

        self.stiftUnten = stiftUnten

        ## Referenz auf das Symbol

        self.symbol = TurtleIntern(self.farbe, self.x, self.y, self.groesse, self.winkel, self.sichtbar)

        Zeichenfenster().BeobachterRegistrieren(self)



    ## Aktionsmethode, die bei jedem Taktschlag ausgeführt wird.

    #  Muss bei Bedarf in einer Unterklasse überschrieben werden.

    def AktionAusfuehren(self):

        pass

        

    ## Aktionsmethode, die bei jedem Tastendruck ausgelöst wird.

    #  Muss bei Bedarf in einer Unterklasse überschrieben werden.

    # @param taste gedrückte Taste        

    def TasteGedrueckt(self, taste):

        #print("Taste gedrueckt: ", taste)

        pass

    

    ## Aktionsmethode, die bei jedem Mausklick ausgelöst wird.

    #  Muss bei Bedarf in einer Unterklasse überschrieben werden.

    # @param button Maustaste (1-links, 2-Mausrad, 3-rechts, 4-Mausrad nach oben, 5-Mausrad nach unten)

    # @param pos Position des Mausklicks    

    def MausGeklickt(self, button, pos):

        #print("Maustaste: ", button, " an Position: ", pos)

        pass

 

    ## Verschiebt die Turtle in die Richtung ihres Winkels.

    # @param laenge Anzahl der Längeneinheiten 

    def Gehen(self,laenge):

        self.symbol.Gehen(laenge)

        self.x = self.symbol.x

        self.y = self.symbol.y

        

    ## Setzt die Position der Turtle (Position der Schwanzspitze). Bei der Positionsänderung wird auch bei abgesenktem Stift keine Linie gezeichnet.

    # @param x x-Position der Schwanzspitze

    # @param y y-Position der Schwanzspitze    

    def PositionSetzen(self, x, y):

        self.x = x

        self.y = y

        self.symbol.PositionSetzen(self.x, self.y)

    

    ## Dreht die Figur

    # @param grad Drehwinkel (mathematisch positiver Drehsinn) im Gradmass         

    def Drehen(self, grad):

        self.winkel = (self.winkel+grad)%360

        self.symbol.WinkelSetzen(self.winkel)



    ## Setzt den Drehwinkel der Turtle.

    # Die Winkelangabe ist in Grad, positive Werte drehen gegen den Uhrzeigersinn, negative Werte drehen im Uhrzeigersinn (mathematisch positiver Drehsinn). 0°: rechts; 90°: oben; 180°: links; 270° unten

    # @param winkel der (neue) Drehwinkel der Turtle         

    def WinkelSetzen(self, winkel):

        self.winkel = winkel%360

        self.symbol.WinkelSetzen(self.winkel)

          



    ## Setzt die Stiftfarbe der Turtle.

    # @param farbe Stiftfarbe der Turtle         

    def FarbeSetzen(self, farbe):

        self.farbe = farbe

        self.symbol.FarbeSetzen(self.farbe)



    ## Entfernt die Turtle aus dem Zeichenfenster.

    def Entfernen(self):

        self.symbol.Entfernen()

        Zeichenfenster().BeobachterEntfernen(self)

        del self



    ## Bringt die Turtle eine Ebene nach vorn.      

    def NachVorneBringen(self):

        self.symbol.NachVorneBringen()



    ## Bringt die Turtle in die vorderste Ebene.    

    def GanzNachVornBringen(self):

        self.symbol.GanzNachVornBringen()

    

    ## Bringt die Turtle eine Ebene nach hinten.    

    def NachHintenBringen(self):

        self.symbol.NachHintenBringen()



    ## Bringt die Turtle in die hinterste Ebene.      

    def GanzNachHintenBringen(self):

        self.symbol.GanzNachHintenBringen()

        

    ## Bringt die Turtle zu ihrem Startpunkt. Die Zeichnung wird dabei gelöscht.

    def ZumStartpunktGehen(self):

        self.symbol.ZumStartpunktGehen()

        self.x = self.symbol.x

        self.y = self.symbol.y

        self.winkel = self.symbol.winkel



    ## Turtle bewegt sich danach, ohne zu zeichnen.        

    def StiftHeben(self):

        self.stiftUnten = False

        self.symbol.StiftHeben()



    ## Turtle wechselt in den Zeichenmodus.          

    def StiftSenken(self):

        self.stiftUnten = True

        self.symbol.StiftSenken()    



    ## Schaltet die Sichtbarkeit der Zeichnung ein oder aus.

    # Erlaubte Parameterwerte: true, false

    # @param sichtbar (neue) Sichtbarkeit der Zeichenfläche       

    def SichtbarkeitSetzen(self, sichtbar):

        self.sichtbar = sichtbar

        self.symbol.SichtbarkeitSetzen(self.sichtbar)



    ## Schaltet die Sichtbarkeit der Zeichenfläche ein oder aus.

    # Erlaubte Parameterwerte: true, false

    # @param sichtbar (neue) Sichtbarkeit der Zeichenfläche der Turtle    

    def SichtbarkeitZeichenflaecheSetzen(self, sichtbar):

        self.symbol.SichtbarkeitZeichenflaecheSetzen(sichtbar)



    ## Liefert den Winkel der Turtle.

    # @return Winkel

    def WinkelGeben(self):

        return self.winkel



    ## Liefert die x-Position der Turtle.

    # @return x-Position     

    def XPositionGeben(self):

        return self.x



    ## Liefert die y-Position der Turtle.

    # @return y-Position        

    def YPositionGeben(self):

        return self.y



    ## Testet, ob die Turtle ein Grafikelement berührt.

    # @return true, wenn die Turtle und eine Grafikfigur überlappen    

    def Beruehrt(self):

        return self.symbol.Beruehrt()



    ## Testet, ob die Turtle mit der Schwanzspitze eine gegebene Farbe berührt

    # @param farbe Farbe, auf die getestet werden soll.

    # @return true wenn ein Objekt mit der Farbe berührt wird.     

    def BeruehrtFarbe(self, farbe):

        return self.symbol.BeruehrtFarbe(farbe)



    ## Testet, ob die Turtle eine Objekt berührt.

    # @param objekt Objekt, mit dem eine Überschneidung geprüft werden soll.

    # @return true wenn das übergebene Objekt mit der Farbe berührt.     

    def BeruehrtObjekt(self, objekt):

        return self.symbol.BeruehrtObjekt(objekt)



    ## Leert die Zeichenfläche der Turtle.

    def Loeschen(self):

        self.symbol.Loeschen()

        

    ## Das gesamte Fenster wird neu gezeichnet.

    # Dies passiert nach einem Durchlauf der Hauptroutine des Programms automatisch.

    # Will man innerhalb einer Methode ein Neuzeichnen veranlassen (z. B. um nach Bewegung eines Objekts auf Berührung zu testen), so kann diese Methode ein Neuzeichnen zu anderer Zeit bewirken.

    def FensterNeuZeichnen():

        self.symbol.FensterNeuZeichnen()