# -- coding: utf-8 --
"""
Created on Sun Feb  20 10:00:00 2022
@author: Klaus Reinold
"""

from __future__ import annotations
from threading import Lock, Thread
from typing import Optional
import pygame, math

TRANS = (1, 1, 1)
WEISS = (255, 255, 255)
ROT = (255, 0, 0)
GRUEN = (0, 255, 0)
BLAU = (0, 0, 255)
GELB = (255,255,0)
MAGENTA = (255,0, 255)
CYAN = (0, 255, 255)
HELLGELB = (255, 255, 128)
HELLGRUEN = (128, 255, 128)
ORANGE = (255, 128,0)
BRAUN = (96, 64, 0)
GRAU = (128, 128, 128)
SCHWARZ =  (0, 0, 0)



class SingletonMeta(type):
    """ 
    Hilfsklasse zur Realisierung des Singleton-Musters, damit zu jeder Zeit nur ein einziges Objekt der Klasse Zeichenfenster existiert. 
    """
    _instanz: Optional[Singleton] = None
    _lock: Lock = Lock()


    def __call__(cls, *args, **kwargs):
        """ 
        Methode sorgt dafür, dass nur ein Objekt der Klasse ausgegeben wird.
        """
        with cls._lock:
            if not cls._instanz:
                cls._instanz = super().__call__(*args, **kwargs)
        return cls._instanz



class Zeichenfenster(metaclass=SingletonMeta):
    """ 
    Klasse zur Steuerung des Zeichenfensters
    """
        
    def __init__(self): 
        """ 
        Der Konstruktor legt das Fenster an und die notwendigen Strukturen zur Verwaltung der Objekte
        """
        #Aufruf des Oberklassenkonstruktors: Thread erzeugen
        super().__init__()
        #Fenstergroesse
        self.FENSTERBREITE = 800
        self.FENSTERHOEHE = 600
        self.FPS = 4
        
        self.schaltflaeche = None
        self.schieberegler = None
        self.buttonaufschrift = "Start"
        

        #Liste aller Figuren und Liste der beobachter
        self.figurenliste = pygame.sprite.RenderUpdates()
        self.beobachter = []
        self.loeschliste = []
        #Attribut zum Pausieren der Animation mittels Start/Stopp-Button
        self.nichtGestoppt = False
        self.fenster = None
        
        
        #Starten des Threads
        #self.start()
        #self.GeschwindigkeitSetzen(0.1)
             
        
    def ObjektEinfuegen(self, figur):
        """ 
        Fügt eine Figur in die Liste der zu verwaltenden Objekte ein
        -- Parameter figur einzufügendes Objekt (interne Klasse)        
        """
        self.figurenliste.add(figur)


    def BeobachterRegistrieren(self, beobachter):
        """ 
        Registriert ein Objekt (Turtle, Figur oder Ereignisbehandlung) als Beobachter ein.
        -- Parameter beobachter einzufügender Beobachter   
        """
        self.beobachter.append(beobachter)
         

    def BeobachterEntfernen(self, beobachter):
        """ 
        Entfernt ein Objekt (Turtle, Figur oder Ereignisbehandlung) als Beobachter.
        -- Parameter beobachter zu entfernender Beobachter   
        """
        self.beobachter.remove(beobachter)   


    def AktionAusfuehren(self):
        """ 
        Informiert die Beobachter (Turtles, Figuren und Ereignisbehandlungs-Objekte) über einem Taktschlag
        """
        kopie_von_beobachterliste = self.beobachter.copy()
        for beobachter in kopie_von_beobachterliste:
            beobachter.AktionAusfuehren()
 

    def MausGeklickt(self, button, pos):
        """ Informiert die Beobachter (Turtles, Figuren und Ereignisbehandlungs-Objekte) über einen Mausklick
        -- Parameter button Maustaste (1-links, 2-Mausrad, 3-rechts, 4-Mausrad nach oben, 5-Mausrad nach unten)
        -- Parameter pos Position des Mausklicks
        """
        x, y = pos
        if x < self.FENSTERBREITE-100 or y < self.FENSTERHOEHE-90:
            kopie_von_beobachterliste = self.beobachter.copy()
            for beobachter in kopie_von_beobachterliste:
                beobachter.MausGeklickt(x, y, button)
                

    def TasteGedrueckt(self, taste):
        """ 
        Informiert die Beobachter (Turtles, Figuren und Ereignisbehandlungs-Objekte) über einen Tastendruck
        -- Parameter taste gedrückte Taste         
        """
        kopie_von_beobachterliste = self.beobachter.copy()
        for beobachter in kopie_von_beobachterliste:
            beobachter.TasteGedrueckt(taste)
            

    def Pausieren(self):
        """ 
        Taktgeber unterbricht Benachrichtigungen der Beobachter.    
        """
        self.nichtGestoppt = False
        
    def Stoppen(self):
        """ 
        Taktgeber unterbricht Benachrichtigungen der Beobachter. 
        """
        self.Pausieren()


    def Starten(self):
        """ 
        Taktgeber nimmt Benachrichtigungen der Beobachter wieder auf.   
        """
        self.nichtGestoppt = True
    
    def ButtonGeben(self):
        """
        Gibt den Button zurück
        --- return Button
        """
        return self.schaltflaeche
    
    def SchieberGeben(self):
        """
        Gibt den Schieberegler zurück
        --- return Schieberegler
        """
        return self.schieberegler 
        
    def TaktdauerSetzen(self, ms):
        """ 
        Methode zum Setzen der Taktdauer
        -- Parameter ms Taktdauer in Millisekunden (Wertebereich 1..1000)       
        """
        if ms >= 1 and ms<=1000:
            self.GeschwindigkeitSetzen(int(round(1000/ms)))
        else:
            print("kein gültiger Wert!")

        
    def GeschwindigkeitSetzen(self, fps):
        """ 
        Methode zum Setzen der Geschwindigkeit
        -- Parameter fps frames per second - Bilder pro Sekunde
        """
        self.FPS = fps
        if not self.schieberegler == None:
            self.schieberegler.WertSetzen(self.FPS)


    def run(self): 
        """
        run-Methode des Threads - enthält die Hauptroutine des Programms         
        """
        #Pygame und Fenster initialisieren
        pygame.init()
        groesse = (self.FENSTERBREITE,self.FENSTERHOEHE)
        self.fenster = pygame.display.get_surface()
        if self.fenster is None:
            self.fenster = pygame.display.set_mode(groesse)
            pygame.display.set_caption("Zeichenfenster")
        else:
            print("Zeichenfenster erst schließen! Mehrfaches Starten führt zu Instabilität. Am besten, du startest den Kernel neu!")
        
        #Entfernung unnoetiger Ereignisse, so dass sie nicht in die Ereignisliste kommen
        pygame.event.set_blocked(pygame.ACTIVEEVENT)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.event.set_blocked(pygame.JOYAXISMOTION)
        pygame.event.set_blocked(pygame.JOYBALLMOTION)
        pygame.event.set_blocked(pygame.JOYHATMOTION)
        pygame.event.set_blocked(pygame.JOYBUTTONUP)
        pygame.event.set_blocked(pygame.JOYBUTTONDOWN)
        pygame.event.set_blocked(pygame.VIDEORESIZE)
        pygame.event.set_blocked(pygame.VIDEOEXPOSE)
        pygame.event.set_blocked(pygame.USEREVENT)
        
        #Taktsteuerung
        clock=pygame.time.Clock()

        #Button und Schieberegler initalisieren
        self.schaltflaeche = self.Button((self.FENSTERBREITE-50,self.FENSTERHOEHE-70),  self.fenster, self)     
        self.schieberegler = self.Schieberegler( "Tempo", self.FPS, 1, 300, self.FENSTERBREITE-100,self.FENSTERHOEHE-50, self.fenster, self)
        #lokales Attribut zum Beenden des Spiels
        nichtBeendet = True
        
    
        #Hauptroutine des Pygames 
        while nichtBeendet:
                
                # Ereignisbehandlung: Durchlaufe alle aktuellen Ereignisse
                for event in pygame.event.get():
                    
                    #Schliessen-Button
                    if event.type==pygame.QUIT:
                        nichtBeendet=False
                    
                    #Maus losgelassen
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.schaltflaeche.mousebuttonup()
                        self.schieberegler.hit = False
                        self.MausGeklickt(event.button, event.pos)
                        
                    #Maus gedrueckt
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if self.schieberegler.button_rect.collidepoint(pos):
                            self.schieberegler.hit = True
                    
                    #Taste gedrueckt
                    elif event.type == pygame.KEYDOWN:
                        self.TasteGedrueckt(pygame.key.name(event.key))
                        
                #Steuerung des Sliders im Menue rechts unten        
                if self.schieberegler.hit:
                    self.schieberegler.move()    
                #Information der Beobachter ueber den Taktschlag
                if self.nichtGestoppt:
                        self.AktionAusfuehren()

                #Löschen von Figuren
                for figur in self.loeschliste:
                    self.figurenliste.remove(figur)
                    self.loeschliste.remove(figur)
                    del figur
                
                #Darstellung des Hintergrunds und der Objekte
                self.FensterNeuZeichnen()
         
                #Wartezeit bis zum nächsten Durchlauf (FPS -> Frames per second)
                clock.tick(self.FPS)
        
        #Schliessen des Fensters nach Abbruch der Hauptroutine         
        pygame.quit()
        self._delete()
        del(self)



    def GanzNachVornBringen(self,figur):
        """ 
        Bringt eine Figur ganz nach vorne. 
        -- Parameter figur Figur, die nach vorne kommt.      
        """
        if self.figurenliste.has(figur):
            self.figurenliste.remove(figur)
            self.figurenliste.add(figur)


    def GanzNachHintenBringen(self,figur):
        """ 
        Bringt eine Figur ganz nach hinten. 
        -- Parameter figur Figur, die nach hinten kommt.         
        """
        if self.figurenliste.has(figur):
            self.figurenliste.remove(figur)
            kopie=self.figurenliste.copy()
            self.figurenliste.empty()
            self.figurenliste.add(figur)
            self.figurenliste.add(kopie)


    def NachHintenBringen(self,figur):
        """
        Bringt eine Figur eine Ebene nach hinten. 
        -- Parameter figur Figur, die nach hinten kommt.
        """
        if self.figurenliste.has(figur):
            liste=self.figurenliste.sprites()
            index_figur = liste.index(figur)
            if index_figur > 0:
                self.figurenliste.empty()
                if index_figur >= 2:
                    for i in range(index_figur-1):
                        figur = liste.pop(0)
                        self.figurenliste.add(figur) 
                self.figurenliste.add(liste.pop(1))
                self.figurenliste.add(liste)
     

    def NachVorneBringen(self,figur):
        """ 
        Bringt eine Figur eine Ebene nach vorne. 
        -- Parameter figur Figur, die nach vorne kommt.        
        """
        if self.figurenliste.has(figur):
          liste=self.figurenliste.sprites()
          index_figur = liste.index(figur)
          if index_figur < len(liste)-1:
            self.figurenliste.empty()
            if index_figur >= 1:
                for i in range(index_figur):
                    figur=liste.pop(0)
                    self.figurenliste.add(figur)
            self.figurenliste.add(liste.pop(1))
            self.figurenliste.add(liste)  


    def Entfernen(self, figur):
        """ 
        Entfernt eine Figur.
        -- Parameter figur Figur, die nach vorne kommt.             
        """
        if(self.figurenliste.has(figur)):
            self.figurenliste.remove(figur)
            
        
    def FensterNeuZeichnen(self):
        """
        Neuzeichnen des Fensters.
        """
        #Darstellung des Hintergrunds und der Objekte
        if not self.fenster is None:
            self.fenster.fill((230,230,230))
            figurenliste = self.figurenliste.copy()
            for figur in figurenliste:   
                figur.Darstellen(self.fenster)
  

            #Darstellung des Menues
            pygame.draw.rect(self.fenster, GRAU, [self.FENSTERBREITE-100,self.FENSTERHOEHE-90, 100,90])
            self.schaltflaeche.draw()
            self.schieberegler.draw()
     
            #Aktualisierung des gesamten Fensters
            if pygame.display.get_active():
                pygame.display.flip()             
    

    class Button():
        """ 
        Klasse zur Beschreibung eines Buttons (für Start/Stop)
        """       
            
        def __init__(self, location, fenster, zeichenfenster):
            """
            Initialisierung des Button
            -- Parameter location Position
            -- Parameter fenster Fenster zur Darstellung
            -- Parameter zeichenfenster Zeichenfenster-Objekt
            """
            self.color = (255,255,255)  # normale Farbe
            self.bg = (255,255,255)  # aktuelle Hintergrundfarbe
            self.fg = (0,0,0)  # Textfarbe
            self.groesse = (90,30)
            self.fenster=fenster
            self.zeichenfenster=zeichenfenster
    
            self.font = pygame.font.SysFont("Arial", 16)
            self.txt = self.zeichenfenster.buttonaufschrift
            self.txt_surf = self.font.render(self.txt, 1, self.fg)
            self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.groesse])
    
            self.surface = pygame.surface.Surface(self.groesse)
            self.rect = self.surface.get_rect(center=location)
        
           
        def draw(self):
            """ 
            Zeichnen des Buttons    
            """
            self.mouseover()
            self.surface.fill(self.bg)
            self.surface.blit(self.txt_surf, self.txt_rect)
            self.fenster.blit(self.surface, self.rect)
 
                
        def mouseover(self):
            """ 
            Reaktion auf Mausberührung    
            """
            self.bg = self.color
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.bg = (200,200,200)  # Farbe bei Mouseover
    
                
        def wechseln(self):
            """ 
            Welchsel zwischen Start und Stopp      
            """
            if self.txt=="Start":                
                self.inBetriebsmodusWechseln()
            else:
                self.inStopmodusWechseln()
            
        
        def inStopmodusWechseln(self):
            """
            Button wechselt in Modus "gestoppt", Anzeige für den Benutzer wird "Start"
            """
            self.txt = "Start"
            self.zeichenfenster.Stoppen()
            self.txt_surf = self.font.render(self.txt, 1, self.fg)
         
        def inBetriebsmodusWechseln(self):
            """
            Button wechselt in Modus "gestoppt", Anzeige für den Benutzer wird "Start"
            """
            self.txt = "Stop"
            self.zeichenfenster.Starten()
            self.txt_surf = self.font.render(self.txt, 1, self.fg)
 
        def mousebuttonup(self):
            """ 
            Reaktion auf Drücken des Buttons          
            """
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                   self.wechseln()
    

    class Schieberegler():
        """ 
        Klasse zur Beschreibung eines Schiebereglers (für Tempo)  
        """
                    
        def __init__(self, name, val, mini, maxi, xpos, ypos, fenster, zeichenfenster):
            """
            Initialisierung des Schiebereglers
            -- Parameter name Beschriftung des Reglers
            -- Parameter val aktueller Wert
            -- Parameter mini minimaler Wert
            -- Parameter maxi maximaler Wert
            -- Parameter xpos x-Position
            -- Parameter ypos y-Position
            -- Parameter fenster Anzeige-Fenster
            -- Parameter zeichenfenster Zeichenfenster-Objekt
            """
            self.val = val  # startwert
            self.maxi = maxi  # maximalwert
            self.mini = mini  # minimumswert
            self.xpos = xpos
            self.ypos = ypos
            self.surf = pygame.surface.Surface((100, 50))
            self.fenster = fenster
            self.hit = False  # zeigt an, ob der Slider gedrückt wird.
            self.font = pygame.font.SysFont("Arial", 12)
            self.txt_surf = self.font.render(name, 1, (0,0,0))
            self.txt_rect = self.txt_surf.get_rect(center=(50, 15))
            self.zeichenfenster = zeichenfenster
    
            # Hintergrund des Sliders #
            self.surf.fill((100, 100, 100))
            pygame.draw.rect(self.surf, GRAU, [0, 0, 100, 50], 3)
            pygame.draw.rect(self.surf, ORANGE, [10, 10, 80, 10], 0)
            pygame.draw.rect(self.surf, WEISS, [10, 30, 80, 5], 0)
    
            self.surf.blit(self.txt_surf, self.txt_rect)  # Anzeigen
    
            # Vordergrund des Sliders #
            self.button_surf = pygame.surface.Surface((20, 20))
            self.button_surf.fill(TRANS)
            self.button_surf.set_colorkey(TRANS)
            pygame.draw.circle(self.button_surf, SCHWARZ, (10, 10), 6, 0)
            pygame.draw.circle(self.button_surf, ORANGE, (10, 10), 4, 0)
                
                
        def draw(self):
            """ 
            Zeichnen des Schiebereglers    
            """
            # statisch
            surf = self.surf.copy()  
            # dynamisch
            pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
            self.button_rect = self.button_surf.get_rect(center=pos)
            surf.blit(self.button_surf, self.button_rect)
            self.button_rect.move_ip((self.xpos, self.ypos))  # Positionieren
            # fenster
            self.fenster.blit(surf, (self.xpos, self.ypos))
     
               
        def move(self):
            """ 
            Bewegung des Knopfes
            """
            self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini
            if self.val < self.mini:
                self.val = self.mini
            if self.val > self.maxi:
                self.val = self.maxi
            self.zeichenfenster.FPS = self.val
    
        def WertSetzen(self, fps):
            """
            Setzen des Werts des Schiebereglers
            -- Parameter fps Frames pro Sekunde
            """
            self.val = fps
            self.zeichenfenster.FPS = self.val
            self.draw()





   
class Intern(pygame.sprite.Sprite):
    """ 
    Interne Oberklasse, erbt von pygame.sprite.Sprite
    """

       
    def __init__(self, farbe, x, y, breite, hoehe, winkel, sichtbar):
        """ Konstruktor der internen Oberklasse
        -- Parameter farbe Farbe des Objekts
        -- Parameter x x-Position
        -- Parameter y y-Position
        -- Parameter breite Breite des Objekts
        -- Parameter hoehe Höhe des Objekts
        -- Parameter winkel Winkel des Objekts
        -- Parameter sichtbar Sichtbarkeit des Objekts
        """
        # Aufruf des Oberklassenkonstruktors
        super().__init__()
        
        Zeichenfenster()
        #Initialisierung der Attribute.
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.farbe = self.FarbeGeben(farbe)
        self.winkel = winkel
        self.sichtbar = True
        
        
        self.image = pygame.Surface([self.breite, self.hoehe])
        self.NeuZeichnen()
        self.NeuPositionieren()
        self.geaendert = False
        self.positionGeaendert = False
        self.winkelGeaendert = False
        
        Zeichenfenster().ObjektEinfuegen(self)
    
        
    def FensterNeuZeichnen(self):
        """ 
        Das gesamte Fenster wird neu gezeichnet.
        Dies passiert nach einem Durchlauf der Hauptroutine des Programms automatisch.
        Will man innerhalb einer Methode ein Neuzeichnen veranlassen (z. B. um nach Bewegung eines Objekts auf Berührung zu testen), so kann diese Methode ein Neuzeichnen zu anderer Zeit bewirken.
        """
        Zeichenfenster().FensterNeuZeichnen()
        
        
        
    def NeuZeichnen(self):
        """ 
        Neuzeichnen des Objekts            
        """
        self.image.fill(TRANS)
        self.image.set_colorkey(TRANS)#Transparente Farbe
        self.geaendert = False
        
        
    def NeuPositionieren(self):
        """
        Neupositionieren des Fensters
        """
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.positionGeaendert = False


    def NeuGedrehtZeichnen(self):
        """ 
        Neuzeichnen für Winkel != 0       
        """
        old_center = self.rect.center
        self.image_gedreht = pygame.transform.rotate(self.image , self.winkel)
        self.rect_gedreht = self.image_gedreht.get_rect()
        self.rect_gedreht.center = old_center  


    def Darstellen(self, fenster):
        """ 
        Darstellen
        -- Parameter fenster Fenster, in dem die Darstellung erfolgt    
        """
        if self.sichtbar:
            if self.geaendert:
                self.NeuZeichnen()
            if self.positionGeaendert:
                self.NeuPositionieren()
            if self.winkelGeaendert:
                self.NeuGedrehtZeichnen()
            self.image.unlock()    
            if self.winkel == 0:
                   fenster.blit(self.image,self.rect)
            else:
                   fenster.blit(self.image_gedreht,self.rect_gedreht) 

        
    def PositionSetzen(self, x, y):
        """ 
        Festlegen der Position des Objekts
        -- Parameter x x-Position
        -- Parameter y y-Position                    
        """
        self.x = x
        self.y = y
        self.positionGeaendert = True
     

    def GroesseSetzen (self, breite, hoehe):
        """ 
        Festlegen der Größe des Objekts
        -- Parameter breite Breite des umgebenden Rechtecks 
        -- Parameter hoehe Höhe des umgebenden Rechtecks          
        """
        self.breite = breite
        self.hoehe = hoehe  
        self.image = pygame.Surface([self.breite, self.hoehe])
        self.geaendert = True
        self.positionGeaendert = True
        if self.winkel > 0:
            self.winkelGeaendert = True

       
    def FarbeSetzen(self, farbe):
        """ 
        Festlegen der Farbe des Objekts
        -- Parameter farbe Farbe des Objekts     
        """
        self.farbe = self.FarbeGeben(farbe)
        self.geaendert = True

       
    def WinkelSetzen(self, winkel):
        """ 
        Festlegen des Winkels des Objekts
        -- Parameter winkel Winkel des Objekts         
        """
        self.winkel = winkel % 360
        self.winkelGeaendert = True
        
        
        
    def SichtbarkeitSetzen(self, sichtbar):
        """ 
        Festlegen der Sichtbarkeit des Objekts
        -- Parameter sichtbar Sichtbarkeit des Objekts         
        """
        self.sichtbar = sichtbar

        
    def Entfernen(self):
        """ 
        Entfernen des Objekts    
        """
        Zeichenfenster().Entfernen(self)
        

        
    def FarbeGeben(self, wert):
        """ 
        Ermittlung des RGB-Farbwertes
        -- Parameter wert Farbe als String (auch RGB wird akzeptiert)       
        """
        if wert in ("weiss", "weiss", "white"):
            return WEISS
        elif wert in ("red", "rot"):
            return ROT
        elif wert in ("gruen", "grün", "green"):
            return GRUEN
        elif wert in ("blue", "blau"):
            return BLAU
        elif wert in ("yellow", "gelb"):
            return GELB
        elif wert in ("magenta", "pink"):
            return MAGENTA
        elif wert == "cyan":
            return CYAN
        elif wert == "hellgelb":
            return HELLGELB
        elif wert in ("hellgruen", "hellgrün"):
            return HELLGRUEN
        elif wert == "orange":
            return ORANGE
        elif wert in ("braun", "brown"):
            return BRAUN
        elif wert in ("grau", "grey"):
            return GRAU
        elif wert in ("transparent", "TRANS"):
            return TRANS
        elif wert in ("black", "schwarz"):
            return SCHWARZ
        elif type(wert) is tuple:
            if (0,0,0) <= wert <= (255,255,255):
                return wert
        else:
            return SCHWARZ
    
        
    def GanzNachVornBringen(self):
        """ 
        Objekt in den Vordergrund bringen    
        """
        Zeichenfenster().GanzNachVornBringen(self)

        
    def NachVorneBringen(self):
        """ 
        Objekt eine Ebene nach vorne bringen           
        """
        Zeichenfenster().NachVorneBringen(self)

        
    def NachHintenBringen(self):
        """ 
        Objekt eine Ebene nach hinten bringen     
        """
        Zeichenfenster().NachHintenBringen(self)

        
    def GanzNachHintenBringen(self):
        """
        Objekt in den Hintergrund bringen     
        """
        Zeichenfenster().GanzNachHintenBringen(self)
    
        
    def EnthaeltFarbe(self, farbe):
        """ 
        Überprüft, ob die gegebene Farbe die Farbe des Objekts ist.
        -- Parameter farbe zu überprüfender Farbwert
        -- return Wert gibt an, ob Farben identisch sind      
        """
        return self.farbe == farbe
        



        

class RechteckIntern(Intern):
    """ 
    Klasse zur Beschreibung des Rechtecks (intern)       
    """
 
        
    def __init__(self, farbe, x, y, breite, hoehe, winkel, sichtbar):
        """ 
        Konstruktor der internen Rechtecksklasse
        -- Parameter farbe Farbe des Objekts
        -- Parameter x x-Position
        -- Parameter y y-Position
        -- Parameter breite Breite des Objekts
        -- Parameter hoehe Höhe des Objekts
        -- Parameter winkel Winkel des Objekts
        -- Parameter sichtbar Sichtbarkeit des Objekts
        """
        super().__init__(farbe, x, y, breite, hoehe, winkel,sichtbar)
    
        
    def NeuZeichnen(self):
        """ 
        Methode zum Zeichnen des internen Rechtecks    
        """
        super().NeuZeichnen()
        pygame.draw.rect(self.image, self.farbe, (0,0,self.breite, self.hoehe))
        if self.winkel != 0:
            super().NeuGedrehtZeichnen()


class BildIntern(Intern):
    """ 
    Klasse zur Beschreibung des Bildes (intern)       
    """
 
        
    def __init__(self, farbe, x, y, winkel, sichtbar, dateiangabe):
        """ 
        Konstruktor der internen Rechtecksklasse
        -- Parameter farbe Farbe des Objekts
        -- Parameter x x-Position
        -- Parameter y y-Position
        -- Parameter breite Breite des Objekts
        -- Parameter hoehe Höhe des Objekts
        -- Parameter winkel Winkel des Objekts
        -- Parameter sichtbar Sichtbarkeit des Objekts
        """
        self.datei = dateiangabe
        super().__init__(farbe, x, y, 100, 100, winkel,sichtbar)
        
        self.x = x
        self.y = y

        self.farbe = self.FarbeGeben(farbe)
        self.winkel = winkel
        self.sichtbar = True
        self.BildSetzen(dateiangabe)
        self.NeuZeichnen()
        self.NeuPositionieren()
        self.geaendert = False
        self.positionGeaendert = False
        self.winkelGeaendert = False
        
        Zeichenfenster().ObjektEinfuegen(self)
        
    def NeuZeichnen(self):
        """ 
        Methode zum Zeichnen des internen Rechtecks    
        """
        super().NeuZeichnen()
        self.image = pygame.transform.scale(pygame.image.load(self.datei),[self.breite, self.hoehe])
        if self.winkel != 0:
            super().NeuGedrehtZeichnen()

    def BildSetzen(self, dateiangabe):
        """
        Methode zum Ändern des Bildes
        """
        self.image = pygame.image.load(dateiangabe) # liefert Surface
        self.datei = dateiangabe
        dim = self.image.get_rect()
        self.breite = dim.width
        self.hoehe=dim.height
        self.NeuZeichnen()
        
    def GroesseSetzen(self,breite, hoehe):
        self.breite = breite
        self.hoehe = hoehe
        self.NeuZeichnen()
            
    def beruehrtPunkt(self, posX, posY):
        return self.rect.collidepoint(posX, posY)

class KreisIntern(Intern):
    """ 
    Klasse zur Beschreibung des Kreises (intern)         
    """

       
    def __init__(self, farbe, x, y, radius,  winkel, sichtbar):
        """ Konstruktor der internen Kreisklasse
        -- Parameter farbe Farbe des Objekts
        -- Parameter x x-Position
        -- Parameter y y-Position
        -- Parameter radius Radius des Objekts
        -- Parameter winkel Winkel des Objekts
        -- Parameter sichtbar Sichtbarkeit des Objekts 
        """
        super().__init__(farbe, x, y, radius* 2, radius * 2, winkel, sichtbar)

        
    def NeuZeichnen(self):
        """ 
        Methode zum Zeichnen des internen Kreises       
        """
        super().NeuZeichnen()
        pygame.draw.ellipse(self.image, self.farbe, (0,0,self.breite, self.hoehe))
        if self.winkel != 0:
            super().NeuGedrehtZeichnen()





class DreieckIntern(Intern):
    """ 
    Klasse zur Beschreibung des Dreiecks (intern)             
    """

       
    def __init__(self, farbe, x, y, breite, hoehe, winkel, sichtbar):
        """ 
        Konstruktor der internen Dreiecksklasse
        -- Parameter farbe Farbe des Objekts
        -- Parameter x x-Position
        -- Parameter y y-Position
        -- Parameter breite Breite des Objekts
        -- Parameter hoehe Höhe des Objekts
        -- Parameter winkel Winkel des Objekts
        -- Parameter sichtbar Sichtbarkeit des Objekts  
        """
        super().__init__(farbe, x, y, breite, hoehe, winkel, sichtbar)

        
    def NeuZeichnen(self):
        """ 
        Methode zum Zeichnen des internen Dreiecks          
        """
        super().NeuZeichnen()
        pygame.draw.polygon(self.image, self.farbe, [(self.breite/2,0),(self.breite, self.hoehe),(0, self.hoehe)])
        if self.winkel != 0:
            super().NeuGedrehtZeichnen()
  

      
 

class TextIntern(Intern):
    """ 
    Klasse zur Beschreibung des Textes (intern)
    """

        
    def __init__(self, farbe, x, y, textgroesse, winkel, sichtbar):
        """ Konstruktor der internen Textklasse
        -- Parameter farbe Farbe des Objekts
        -- Parameter x x-Position
        -- Parameter y y-Position
        -- Parameter textgroesse Größe des Texts
        -- Parameter winkel Winkel des Objekts
        -- Parameter sichtbar Sichtbarkeit des Objekts  
        """
        self.groesse = textgroesse
        self.textinhalt = "Text"
        self.geaendert = True
        super().__init__(farbe, x, y, 0, 0, winkel,sichtbar)

       
    def TextSetzen(self, text):
        """
        Methode zum Festlegen des Textes
        -- Parameter text darzustellender Text    
        """
        self.textinhalt = text
        self.geaendert = True

        
    def TextGroesseSetzen(self, groesse):
        """ 
        Festlegung der Textgröße
        -- Parameter groesse Schriftgröße        
        """
        self.groesse = groesse
        self.geaendert = True

        
    def TextVergroessern(self):
        """ 
        Vergrößerung der Schrift       
        """
        if self.groesse <= 10:
            self.groesse += 1
        elif self.groesse <= 40:
            self.groesse += 2
        else:
            self.groesse += 4
        self.geaendert = True
 
 
    def TextVerkleinern(self):
        """ 
        Verkleinerung der Schrift        
        """
        if self.groesse <= 10:
            self.groesse -= 1
        elif self.groesse <= 40:
            self.groesse -= 2
        else:
            self.groesse -= 4
        if self.groesse < 1:
            self.groesse = 1
        self.geaendert = True

        
    def NeuZeichnen(self):
        """ 
        Methode zum Zeichnen des internen Textes          
        """
        font = pygame.font.SysFont("Arial", self.groesse)
        self.text = font.render(self.textinhalt, True, self.farbe)
        self.textRect = self.text.get_rect()
        self.textRect.topleft = (self.x,self.y)
        if self.winkel != 0:
            self.NeuGedrehtZeichnen()
            
       
    def NeuGedrehtZeichnen(self):
        """
        Methode zum Zeichnen des internen Textes bei Winkel != 0    
        """
        old_center = self.textRect.center
        self.textGedreht = pygame.transform.rotate(self.text, self.winkel)
        self.textRectGedreht=self.textGedreht.get_rect()
        self.textRectGedreht.center = old_center 
    
        
    def Darstellen(self, fenster):
        """ 
        Darstellen des Textes im Fenster
        -- Parameter fenster      
        """
        if self.geaendert:
            self.geaendert = False
            self.NeuZeichnen()
        if self.positionGeaendert:
                self.NeuPositionieren()  

        if self.winkel == 0:
               fenster.blit(self.text,(self.x, self.y))
        else:
               self.NeuGedrehtZeichnen()
               fenster.blit(self.textGedreht,self.textRectGedreht) 
  
    def NeuPositionieren(self):
        """
        Neupositionieren des Fensters
        """
        self.textRect = self.text.get_rect()
        self.textRect.topleft = (self.x,self.y)

        self.positionGeaendert = False
        
 

    
class FigurIntern(Intern):
    """
    Klasse zur Beschreibung der Figur (intern)
    """
    

    def __init__(self, x, y, groesse, winkel, sichtbar):
        """ 
        Konstruktor der internen Figurklasse
        -- Parameter x x-Position
        -- Parameter y y-Position
        -- Parameter groesse Größe der Figur
        -- Parameter winkel Winkel des Objekts
        -- Parameter sichtbar Sichtbarkeit des Objekts 
        """
        self.xD = x
        self.yD = y
        self.homeX = x
        self.homeY = y
        self.homeWinkel = 0
        self.figurenliste = []
        self.IstStandardfigur = True
        super().__init__((255,255,255), x, y, groesse, groesse, winkel, sichtbar)
        self.farbliste = []
        self.bausteine = []
        self.StandardfigurErzeugen() 
        self.groesse = groesse
        self.maxVal = 50


    def PositionSetzen(self, x, y):
        """ 
        Setzt die Position der Figur.
        -- Parameter x x-Position der Mitte der Figur
        -- Parameter y y-Position der Mitte der Figur    
        """
        super().PositionSetzen(x, y)
        self.xD = x
        self.yD = y
        self.positionGeaendert = True

        
    def Gehen(self,laenge):
        """ 
        Verschiebt die Figur in die Richtung ihres Winkels.
        -- Parameter laenge Anzahl der Längeneinheiten   
        """
        neuX = self.xD + math.cos(self.winkel*math.pi/180)*laenge
        neuY = self.yD - math.sin(self.winkel*math.pi/180)*laenge
        self.xD = neuX
        self.yD = neuY
        self.x = round(neuX)
        self.y = round(neuY)
        self.positionGeaendert  = True        

        
    def GroesseSetzen (self, groesse):
        """ 
        Setzt die Größe der Figur.
        -- Parameter groesse Größe des umgebenden Quadrats          
        """
        super().GroesseSetzen(int(groesse*self.maxVal/50),int(groesse*self.maxVal/50)) 
        self.groesse = groesse
        self.FigurNeuAufbauen()
    
    def FigurNeuAufbauen(self):
        self.figurenliste.clear()
        if self.IstStandardfigur:
            self.StandardfigurErzeugen()
        else:
            for element in self.bausteine:
                if element[0]=="Rechteck":
                    x = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[1]/100+self.groesse/2))
                    y = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[2]/100+self.groesse/2))
                    breite = int(round(self.groesse*element[3]/100))
                    hoehe = int(round(self.groesse*element[4]/100))
                    farbeCodiert=element[5]
                    string =  "pygame.draw.rect(self.image,"+ str(farbeCodiert)+", ("+str(x)+","+str(y)+","+str(breite)+", "+str(hoehe)+"))"
                if element[0]=="Ellipse":
                    x = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[1]/100+self.groesse/2))
                    y = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[2]/100+self.groesse/2))
                    breite = int(round(self.groesse*element[3]/100))
                    hoehe = int(round(self.groesse*element[4]/100))
                    farbeCodiert=element[5]
                    string =  "pygame.draw.ellipse(self.image,"+ str(farbeCodiert)+", ("+str(x)+","+str(y)+","+str(breite)+", "+str(hoehe)+"))"
                if element[0]=="Dreieck":
                    x1 = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[1]/100+self.groesse/2))
                    x2 = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[2]/100+self.groesse/2))
                    x3 = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[3]/100+self.groesse/2))
                    y1 = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[4]/100+self.groesse/2))
                    y2 = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[5]/100+self.groesse/2))
                    y3 = int(round((self.maxVal*self.groesse/50-self.groesse)/2+self.groesse*element[6]/100+self.groesse/2))
                    farbeCodiert=element[7]
                    string =  "pygame.draw.polygon(self.image,"+ str(farbeCodiert)+", [("+str(x1)+","+str(y1)+"),("+str(x2)+", "+str(y2)+"),("+str(x3)+","+str(y3)+")])"
                self.figurenliste.append(string)
        self.NeuZeichnen()
        self.PositionSetzen(self.xD,self.yD)
    
        
    def ZumStartpunktGehen(self):
        """ 
        Bringt die Figur zu ihrem Startpunkt.          
        """
        self.x = self.homeX
        self.y = self.homeY
        self.xD = self.x
        self.yD = self.y
        self.winkel = self.homeWinkel
        self.positionGeaendert = True

       
    def NeuZeichnen(self):
        """ 
        Zeichnet die Figur neu im Fenster.        
        """
        super().NeuZeichnen()  
        for codezeile in self.figurenliste:
           exec(codezeile) 
        if self.winkel != 0:
            super().NeuGedrehtZeichnen()
        self.mask = pygame.mask.from_surface(self.image)
            
            
        
    def NeuPositionieren(self):
        """ 
        Positioniert die Turtle neu.
        """
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.positionGeaendert = False
            
        
        
    def Beruehrt(self):
        """ 
        Testet, ob die Figur eine andere Figur (Turtle, Rechteck,...) berührt.
        -- return True, wenn die Figur und eine Grafikfigur überlappen     
        """
        sprites_list = Zeichenfenster().figurenliste.copy()
        sprites_list.remove(self)
        for figur in sprites_list:
            if not (isinstance(figur, TextIntern)):
                if not(pygame.sprite.collide_mask(self, figur) is None):
                    return True
        return False

        
    def BeruehrtFarbe(self, farbe):
        """ 
        Testet, ob die Figur eine Objekt berührt, das die gegebene Farbe enthält.
        (die Farbe muss nicht unbedingt sichtbar oder direkt berührt werden)
        -- Parameter farbe Farbe, auf die getestet werden soll.
        -- return True wenn ein Objekt mit der Farbe berührt wird.      
        """
        sprites_list = Zeichenfenster().figurenliste.copy()
        sprites_list.remove(self)
        for figur in sprites_list:
            if not (isinstance(figur, TextIntern)):
                if (not(pygame.sprite.collide_mask(self, figur) is None)):
                    if figur.EnthaeltFarbe(self.FarbeGeben(farbe)):
                        return True
        return False

        
    def BeruehrtObjekt(self, objekt):
        """ 
        Testet, ob die Figur eine Objekt berührt.
        -- Parameter objekt Objekt, mit dem eine Überschneidung geprüft werden soll.
        -- return True wenn das übergebene Objekt mit der Farbe berührt.             
        """
        if isinstance(objekt, TextIntern):
            return False
        return not (pygame.sprite.collide_mask(self, objekt.symbol) is None)

        
    def StandardfigurErzeugen(self):
        """ 
        Erzeugt eine Standardfigur
        """
        if not self.IstStandardfigur:
            self.bausteine.clear()
            self.figurenliste.clear()
            self.image.fill(TRANS)
            self.IstStandardfigur = True
        self.figurenliste.append("pygame.draw.polygon(self.image, GELB, [(0, 0),(self.breite, self.hoehe/2),(0, self.hoehe)])")
        self.figurenliste.append("pygame.draw.ellipse(self.image, BLAU, (self.breite/2-4, self.hoehe/2 -4,8,8))")
        self.farbliste = []
        self.farbliste.append(GELB)
        self.farbliste.append(BLAU)
        self.geaendert  = True
        self.maxVal = 50

       
    def FigurteilFestlegenRechteck(self,x, y, breite, hoehe, farbe):
        """ Erzeugt ein neues, rechteckiges Element.
        Alle Werte beziehen sich auf eine Figur der Größe 100x100 und den Koordinaten (0|0) in der Mitte des Quadrats
        -- Parameter x x-Wert der linken oberen Ecke des Rechtecks innerhalb der Figur (-50<=x<=50)
        -- Parameter y y-Wert der linken oberen Ecke des Rechtecks innerhalb der Figur (-50<=y<=50)
        -- Parameter breite Breite des Rechtecks innerhalb der Figur (0<=breite<=50-x)
        -- Parameter hoehe Höhe des Rechtecks innerhalb der Figur (0<=hoehe<=50-x)
        -- Parameter farbe Farbe des Figurelements
        """
        if self.IstStandardfigur:
            self.figurenliste.clear()
            self.image.fill(TRANS)
            self.IstStandardfigur = False
            self.farbliste = []
 
        farbeCodiert = self.FarbeGeben(farbe)
        if not farbeCodiert in self.farbliste:
            self.farbliste.append(farbeCodiert)
        self.bausteine.append(["Rechteck", x, y, breite, hoehe, farbeCodiert])    
        

        if -x > self.maxVal:
            self.maxVal = -x 
            
            super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
        if -y > self.maxVal:
            self.maxVal = -y
            super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
        if x+breite > self.maxVal:
            self.maxVal = x+breite
            super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
        if y+hoehe > self.maxVal:
            self.maxVal = y+hoehe
            super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
        
      
        self.FigurNeuAufbauen()
        


        
    def FigurteilFestlegenEllipse(self, x, y, breite, hoehe, farbe):
        """ Erzeugt ein neues, elliptisches Element.
        Alle Werte beziehen sich auf eine Figur der Größe 100x100 und den Koordinaten (0|0) in der Mitte des Quadrats
        -- Parameter x x-Wert der linken oberen Ecke des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (-50<=x<=50)
        -- Parameter y y-Wert der linken oberen Ecke des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (-50<=y<=50)
        -- Parameter breite Breite des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (0<=breite<=50-x)
        -- Parameter hoehe Höhe des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (0<=hoehe<=50-x)
        -- Parameter farbe Farbe des Figurelements                    
        """
        if(self.IstStandardfigur):
            self.figurenliste.clear()
            self.image.fill(TRANS)
            self.IstStandardfigur = False
            self.farbliste = []
         
        farbeCodiert = self.FarbeGeben(farbe)
        if not farbeCodiert in self.farbliste:
            self.farbliste.append(farbeCodiert)
        self.bausteine.append(["Ellipse", x, y, breite, hoehe, farbeCodiert])
            
        if -x > self.maxVal:
            self.maxVal = -x 
            super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
        if -y > self.maxVal:
            self.maxVal = -y
            super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
        if x+breite > self.maxVal:
            self.maxVal = x+breite
            super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
        if y+hoehe > self.maxVal:
            self.maxVal = y+hoehe
            super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
    
        self.FigurNeuAufbauen() 

       
    def FigurteilFestlegenDreieck(self, x1, y1 ,x2, y2, x3, y3, farbe):
        """ Erzeugt ein neues, dreieckiges Element einer eigenen Darstellung der Figur.
        Die Werte müssen passend zur Größe der Figur gewählt werden (Standardwert: 40) 
        -- Parameter x1 x-Wert des ersten Punktes innerhalb der Figur (-50<=x1<=50)
        -- Parameter y1 y-Wert des ersten Punktes innerhalb der Figur (-50<=y1<=50)
        -- Parameter x2 x-Wert des zweiten Punktes innerhalb der Figur (-50<=x2<=50)
        -- Parameter y2 y-Wert des zweiten Punktes innerhalb der Figur (-50<=y2<=50)
        -- Parameter x3 x-Wert des dritten Punktes innerhalb der Figur (-50<=x3<=50)
        -- Parameter y3 y-Wert des dritten Punktes innerhalb der Figur (-50<=y3<=50)
        -- Parameter farbe Farbe des Figurelements         
        """   
        if(self.IstStandardfigur):
            self.figurenliste.clear()
            self.image.fill(WEISS)
            self.IstStandardfigur = False
            self.farbliste = []

        farbeCodiert = self.FarbeGeben(farbe)      
        if not farbeCodiert in self.farbliste:
            self.farbliste.append(farbeCodiert)
        self.bausteine.append(["Dreieck", x1, x2, x3, y1, y2, y3, farbeCodiert])
        
        if self.maxVal<-x1:
            self.maxVal = -x1
        if self.maxVal<x1:
            self.maxVal = x1    
        if self.maxVal<-x2:
            self.maxVal = -x2
        if self.maxVal<x2:
            self.maxVal = x2   
        if self.maxVal<-x3:
            self.maxVal = -x3
        if self.maxVal<x3:
            self.maxVal = x3    
        if self.maxVal<-y1:
            self.maxVal = -y1
        if self.maxVal<y1:
            self.maxVal = y1
        if self.maxVal<-y2:
            self.maxVal = -y2
        if self.maxVal<y2:
            self.maxVal = y2   
        if self.maxVal<-y3:
            self.maxVal = -y3
        if self.maxVal<y3:
            self.maxVal = y3 
        
        super().GroesseSetzen(int(self.groesse*self.maxVal/50)+1,int(self.groesse*self.maxVal/50)+1)
       
        self.FigurNeuAufbauen()


    def EnthaeltFarbe(self, farbe):
        """ 
        Testet, ob die Figur die Farbe enthält.   
        -- Parameter farbe zu überprüfende Farbe
        -- return wahr, wenn die Farbe vorhanden ist.
        """
        return self.FarbeGeben(farbe) in self.farbliste
    

    
    
    

class TurtleIntern(Intern):
    """ 
    Klasse zur Beschreibung der Turtle (intern)         
    """
    
        
    def __init__(self, farbe, x, y, groesse, winkel, sichtbar):
        """ 
        Initialisierungsmethode verwaltet die Attribute für Position und Aussehen.
        """
        self.xD = x
        self.yD = y
        self.homeX = x
        self.homeY = y
        self.homeWinkel = 0
        self.stiftUnten = True
        self.farbliste = []
        self.zeichenflaeche = pygame.Surface([Zeichenfenster().FENSTERBREITE, Zeichenfenster().FENSTERHOEHE])
        self.zeichenflaeche.fill(TRANS)#transparene Füllung
        self.zeichenflaeche.set_colorkey(TRANS)#transparente Farbe
        self.sichtbarkeitZeichenflaeche = True
        self.schwanzspitze = Schwanzspitze()
        self.schwanzspitze.PositionSetzen(x, y)
        super().__init__(farbe, x, y, 60, 25, winkel, sichtbar)   

       
    def PositionSetzen(self, x, y):
        """ 
        Setzt die Position der Turtle (Position der Schwanzspitze). Bei der Positionsänderung wird auch bei abgesenktem Stift keine Linie gezeichnet.
        -- Parameter x x-Position der Schwanzspitze
        -- Parameter y y-Position der Schwanzspitze    
        """
        super().PositionSetzen(x, y)
        self.xD = x
        self.yD = y
        self.schwanzspitze.rect.topleft = (self.x, self.y)
        self.positionGeaendert = True

        
    def Gehen(self,laenge):
        """ 
        Verschiebt die Turtle in die Richtung ihres Winkels.
        -- Parameter laenge Anzahl der Längeneinheiten         
        """
        neuX = self.xD + math.cos(self.winkel*math.pi/180)*laenge
        neuY = self.yD - math.sin(self.winkel*math.pi/180)*laenge
        if self.stiftUnten:
            pygame.draw.line(self.zeichenflaeche, self.farbe, (self.x, self.y), (round(neuX), round(neuY)))
        self.xD = neuX
        self.yD = neuY
        self.x = round(neuX)
        self.y = round(neuY)
        self.schwanzspitze.PositionSetzen(self.x, self.y)
        self.positionGeaendert  = True
        

        
    def StiftHeben(self):
        """ 
        Turtle bewegt sich danach, ohne zu zeichnen.         
        """
        self.stiftUnten = False

        
    def StiftSenken(self):
        """ 
        Turtle wechselt in den Zeichenmodus.       
        """
        self.stiftUnten = True
 
        
    def ZumStartpunktGehen(self):
        """ 
        Turtle geht zum Startpunkt         
        """
        self.x = self.homeX
        self.y = self.homeY
        self.xD = self.x
        self.yD = self.y
        self.winkel = self.homeWinkel
        self.schwanzspitze.rect.topleft = (self.x, self.y)
        self.positionGeaendert = True
        
       
    def SichtbarkeitZeichenflaecheSetzen(self, wert):
        """ 
        Schaltet die Sichtbarkeit der Zeichnung ein oder aus.
        Erlaubte Parameterwerte: true, false
        -- Parameter wert (neue) Sichtbarkeit der Zeichenfläche  
        """
        self.sichtbarkeitZeichenflaeche = wert
    
        
    def Beruehrt(self):
        """ 
        Testet, ob die Turtle ein Grafikelement berührt.
        -- return True, wenn die Turtle und eine Grafikfigur überlappen          
        """
        sprites_list = Zeichenfenster().figurenliste.copy()
        sprites_list.remove(self)
        for figur in sprites_list:
            if not (isinstance(figur, TextIntern)):
                if not(pygame.sprite.collide_mask(self.schwanzspitze, figur) is None):
                    return True
        return False

        
    def BeruehrtFarbe(self, farbe):
        """ 
        Testet, ob die Turtle mit der Schwanzspitze eine gegebene Farbe berührt
        -- Parameter farbe Farbe, auf die getestet werden soll.
        - return True wenn ein Objekt mit der Farbe berührt wird.    
        """
        if 22.5 <= self.winkel < 67.5:
            x = self.x - 2
            y = self.y + 2
        elif 67.5 <= self.winkel < 112.5:
            x = self.x
            y = self.y + 2
        elif 112.5 <= self.winkel < 157.5:
            x = self.x + 2
            y = self.y + 2
        elif 157.5 <= self.winkel < 202.5:
            x = self.x + 2
            y = self.y
        elif 202.5 <= self.winkel < 247.5:
            x = self.x + 2
            y = self.y - 2
        elif 247.5 <= self.winkel < 292.5:
            x = self.x
            y = self.y - 2
        elif 292.5 <= self.winkel < 337.5:
            x = self.x - 2
            y = self.y - 2
        else:
            x = self.x - 2
            y = self.y      
        if Zeichenfenster().fenster is None:
            return False
        if not (x < 0 or y < 0 or x > Zeichenfenster().FENSTERBREITE or y > Zeichenfenster().FENSTERHOEHE):
            wert1 = Zeichenfenster().fenster.get_at((x,y))
        else:
            return False
        wert2 = self.FarbeGeben(farbe)
        for i in range(3):
            if(wert1[i]!=wert2[i]):
                return False
        return True

        
    def BeruehrtObjekt(self, objekt):
        """ 
        Testet, ob die Turtle eine Objekt berührt.
        -- Parameter objekt Objekt, mit dem eine Überschneidung geprüft werden soll.
        -- return true wenn das übergebene Objekt mit der Farbe berührt.                 
        """
        if (isinstance(objekt, TextIntern)):
            return True
        return not (pygame.sprite.collide_mask(self.schwanzspitze, objekt.symbol) is None)
        
        
    def EnthaeltFarbe(self, farbe):
        """ 
        Testet, ob die Turtle eine Farbe enthält.
        -- Parameter farbe Farbe, die geprüft werden soll.
        -- return true wenn die Turtle die Farbe enthält.      
        """
        EnthaeltFarbe = False
        if self.FarbeGeben(farbe) in self.Farbliste:
            EnthaeltFarbe = True
        if self.FarbeGeben(farbe) == self.Farbe:
            EnthaeltFarbe = True
        return EnthaeltFarbe

        
    def NeuZeichnen(self):
        """ 
        Zeichnet die Turtle neu.
        """
        super().NeuZeichnen()
        #Kopf
        pygame.draw.ellipse(self.image, GRUEN, (50,7,10, 12))
        #Beine
        pygame.draw.ellipse(self.image, GRUEN, (36,0,8, 25))
        pygame.draw.ellipse(self.image, GRUEN, (44,0,8, 25))
        #Augen
        pygame.draw.ellipse(self.image, self.farbe, (55,9,3, 2))
        pygame.draw.ellipse(self.image, self.farbe, (55,14,3, 2))
        #Schwanz
        pygame.draw.ellipse(self.image, self.farbe, (30,10,10, 5))
        #Rumpf
        pygame.draw.ellipse(self.image, BRAUN, (32,2,24, 21))
        self.schwanzspitze.NeuZeichnen(self.x, self.y, self.farbe)
        self.farbliste.append(GRUEN)
        self.farbliste.append(BRAUN)
      
        if self.winkel != 0:
            super().NeuGedrehtZeichnen()

        
    def NeuPositionieren(self):
        """ 
        Positioniert die Turtle neu.
        """
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.positionGeaendert = False
                  
  

        
    def Darstellen(self, fenster):
        """ 
        Stellt die Turtle dar.
        -- Parameter fenster Fenster zur Darstellung         
        """
        if self.sichtbarkeitZeichenflaeche:
            fenster.blit(self.zeichenflaeche,self.zeichenflaeche.get_rect())
        #self.schwanzspitze.Darstellen(fenster)
        fenster.blit(self.schwanzspitze.image,self.schwanzspitze.image.get_rect())
        super().Darstellen(fenster)

        
    def Loeschen(self):
        """ 
        Löscht die Zeichenfläche.        
        """
        self.zeichenflaeche.fill(TRANS)


class Schwanzspitze(pygame.sprite.Sprite):
    """ 
    Klasse zur Beschreibung der Schwanzspitze der Turtle (intern)          
    """

            
    def __init__(self):
        """ 
        Der Konstruktor erzeugt das Objekt und verwaltet die Attribute für Position und Aussehen.    
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5, 5])
        self.image.fill(ROT)
        self.rect = self.image.get_rect()
        
           
    def PositionSetzen(self, x, y):
         """ 
         Setzt die Position der  Schwanzspitze)
         -- Parameter x x-Position der Schwanzspitze
         -- Parameter y y-Position der Schwanzspitze            
         """
         self.rect.topleft = (x,y)

            
    def NeuZeichnen(self,x,y, farbe):
        """ 
        Zeichnet die Turtle neu.                
        """
        self.image.fill((255,255,255))
        self.image.set_colorkey(TRANS)#Transparente Farbe
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        pygame.draw.rect(self.image, farbe, (0,0,1, 1))
                
                
    
       
    
    