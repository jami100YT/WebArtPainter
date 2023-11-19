import keyboard
import pyautogui
from PIL import Image

class Paint:
    def __init__(self):
        self.image_path = None
        self.image = None
        self.pixel_data = None
        self.currentColor = (None, None, None)
    
        self.colorPositions = {
            "main": None,
            "exitColors": None,
            "R": None,
            "G": None,
            "B": None
        }

        self.canvasPositions = {
            "width": None,
            "height": None,
            "leftTop": None,
            "rightTop": None,
            "rightBottom": None,
            "leftBottom": None
        }

        self.calibration = 1
        self.calibrationMax = 2
        #keyboard.on_press_key('m', self.calibrate_mouse_position)

    def get_mouse_position(self):
        # Gib die aktuelle Mausposition zurück
        return pyautogui.position()
    
    def start_calibration(self):
        self.calibrate_mouse_positions()

    def calibrate_mouse_positions(self):
        self.calibrate_color_positions()
        self.calibrate_canvas()

    def stop(e, two):
        print("idk")
        keyboard.unhook_all()
        exit(0)


    def calibrate_canvas(self):
        print(f"Kalibrierung des Canvas ({self.calibration}/{self.calibrationMax})\n")
        print('Drücke "m" um [leftTop] des Canvas zu kalibrieren.')
        keyboard.wait("m")
        pyautogui.click()
        pyautogui.mouseDown()

        self.canvasPositions["leftTop"] = self.get_mouse_position()
        self.canvasPositions["rightTop"]: pyautogui.Point = pyautogui.Point(self.canvasPositions["leftTop"].x + self.image.height, self.canvasPositions["leftTop"].y)
        pyautogui.mouseDown()
        pyautogui.moveTo(self.canvasPositions["rightTop"])

        self.canvasPositions["rightBottom"]: pyautogui.Point = pyautogui.Point(self.canvasPositions["rightTop"].x, self.canvasPositions["rightTop"].y + self.image.height)
        pyautogui.moveTo(self.canvasPositions["rightBottom"])

        self.canvasPositions["leftBottom"]: pyautogui.Point = pyautogui.Point(self.canvasPositions["leftTop"].x, self.canvasPositions["rightBottom"].y)
        pyautogui.moveTo(self.canvasPositions["leftBottom"])
        pyautogui.moveTo(self.canvasPositions["leftTop"])
        pyautogui.mouseUp()


        answer = input("Ist der Ramen 100% sichtbar im Canvas? ").lower()
        if(answer in ["yes", "y", "ja", "j"]):
            print("Canvas Kalibrierung abgeschlossen!\n\n")
            self.calibration = self.calibration + 1
        elif (answer in ["no", "n", "nein"]):
            print("Kalibrieung Fehlgeschlagen. Versuche erneut.")
            self.calibrate_canvas()


    def calibrate_color_positions(self):
        print(f"Kalibrierung der Color Positions ({self.calibration}/{self.calibrationMax})\n")
        count = 1
        max = len(self.colorPositions)
        for point in self.colorPositions:
            print(f'Drücke "m" um [{point}] zu kalibrieren. ({count}/{max})')
            keyboard.wait("m")
            self.colorPositions[point] = self.get_mouse_position()
            count = count + 1
        self.changeColor(255, 0, 0)

        anwser = input("Wurde die Farbe Rot ausgewählt? ").lower()
        if(anwser in ["y", "yes", "ja", "j"]):
            print("Kalibrierung der Color points abgeschlossen!\n\n")
            self.calibration = self.calibration + 1
        elif (anwser in ["n", "no", "nein"]):
            print("Kalibrierung fehgeschlagen. Versuche erneut")
            self.calibrate_color_positions()


    def changeColor(self, R, G, B):
        # Color Menu öffnen
        pyautogui.moveTo(self.colorPositions["main"])
        pyautogui.click()

        # R Wert eintragen
        pyautogui.moveTo(self.colorPositions["R"])
        pyautogui.click()
        pyautogui.typewrite(str(R))

        # G Wert eintragen
        pyautogui.moveTo(self.colorPositions["G"])
        pyautogui.click()
        pyautogui.typewrite(str(G))

        # B Wert eintragen
        pyautogui.moveTo(self.colorPositions["B"])
        pyautogui.click()
        pyautogui.typewrite(str(B))
        
        # Color Menu verlassen
        pyautogui.moveTo(self.colorPositions["exitColors"])
        pyautogui.click()

    def change_image(self, path):
        try:
            self.image_path = path
            self.image = Image.open(self.image_path)
            self.pixel_data = list(self.image.getdata())
            self.canvasPositions["width"] = self.image.width
            self.canvasPositions["height"] = self.image.height
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")
            exit(0)

    def drawImage(self):
        current_color = None
        # Durch jede Zeile des Bildes iterieren
        for y in range(self.image.height):
            # Die aktuelle Zeile extrahieren
            current_row = self.pixel_data[y * self.image.width:(y + 1) * self.image.width]

            # Initialisierung von Variablen
            #current_color = current_row[0]
            if(current_color != current_row[y]):
                self.changeColor(*current_row[y])
                current_color = current_row[y]
            start_pixel = 0
            start_postion: pyautogui.Point = self.canvasPositions["leftTop"]

            # Durch die Pixel der aktuellen Zeile iterieren und Farbänderungen erkennen
            for i, pixel in enumerate(current_row):
                if keyboard.is_pressed("esc"):
                    print("Das Programm wurde durch Drücken der Esc-Taste beendet.")
                    return
                if pixel != current_color:
                    # Farbänderung feststellen
                    end_pixel = i - 1
                    pixels_to_move = abs(end_pixel - start_pixel)
                    if pixels_to_move == 0:
                        pixels_to_move = 1

                    # Simuliere Cursor-Verschiebung
                    pyautogui.mouseUp()
                    self.changeColor(*pixel)
                    pyautogui.moveTo(start_postion.x + start_pixel, start_postion.y + y)
                    pyautogui.click()
                    pyautogui.mouseDown()
                    pyautogui.move(pixels_to_move, 0)
                    pyautogui.mouseUp()
                    print(f"Zeile: {y} Mauszeiger wurde um {pixels_to_move} nach rechts verschoben || moveTo({start_postion.x + start_pixel}|{start_postion.y + y}) move({pixels_to_move}|{0}) mousePos({self.get_mouse_position().x}|{self.get_mouse_position().y})")

                    # Aktualisiere die aktuellen Variablen
                    start_pixel = i
                    current_color = pixel

            # Letzte Farbänderung ausgeben
            pixels_to_move = abs(self.image.width - 1 - start_pixel)
            if pixels_to_move == 0:
                pixels_to_move = 1
            pyautogui.moveTo(start_postion.x + start_pixel, start_postion.y + y)
            pyautogui.click()
            pyautogui.mouseDown()
            pyautogui.move(pixels_to_move, 0)
            pyautogui.mouseUp()
            print(f"Zeile: {y} Mauszeiger wurde um {pixels_to_move} nach rechts verschoben || moveTo({start_postion.x + start_pixel}|{start_postion.y + y}) move({pixels_to_move}|{0}) mousePos({self.get_mouse_position().x}|{self.get_mouse_position().y})")

            
