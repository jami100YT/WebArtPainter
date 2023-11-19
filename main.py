from paint import Paint
if __name__ == "__main__":
    # Erstelle eine Instanz der Klasse und starte die Kalibrierung
    tracker = Paint()
    tracker.change_image("image.png")
    tracker.start_calibration()
    tracker.drawImage()
    #tracker.drawBlackAndWhiteImage()
    