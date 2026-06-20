"""
Mission: Schule überleben
Gigathon 2026 - Hannes Meinen
"""
import random
import os
import sys

def clear_screen():
    #Konsole leeren (Windows und Mac/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')

def hohe_zahl_eingabe(prompt, default=30, min_val=None, max_val=None):
    eingabe = input(prompt).strip()
    
    if not eingabe:
        return default
    
    try:
        wert = int(eingabe)
        if min_val is not None and wert < min_val:
            print(f"Zu klein. Nehme Minimum: {min_val}")
            return min_val
            """
    if wert < min_val:
    print("Zu klein! Nehme " + str(min_val))  # String + statt f"..." return min_val
    """
           
        if max_val is not None and wert > max_val:
            print(f"Zu groß. Nehme Maximum: {max_val}")
            return max_val
        return wert
    except ValueError:
        print(f"Ungültige Eingabe. Nutze Standardwert: {default}")
        return default

def show_intro():
    print("=" * 65)
    print("        MISSION: SCHULE ÜBERLEBEN")
    print("=" * 65)
    print("Ziel: Bring das Dokument zum Sekretariat.")
    print("Problem: Lehrer, Hausmeister und deine Nerven...\n")

def generate_world(size):
    #Erstellt Kioske, Hausmeister etc. Random Positionen
    objekte = []
    
    # 3 Kioske für Nerven-Boost
    for _ in range(3):
        objekte.append({
            'pos_x': random.randint(-size, size),
            'pos_y': random.randint(-size, size),
            'type': 'kiosk',
            'name': 'Schulkiosk',
            'used': False
        })
    
    # 3 Hausmeister als Hindernis  
    for _ in range(3):
        objekte.append({
            'pos_x': random.randint(-size, size),
            'pos_y': random.randint(-size, size),
            'type': 'janitor',
            'name': 'Herr Krause',
            'used': False
        })
        #print("Hausmeister gespawnt")
    
    # 2 Spicker-Verstecke
    for _ in range(2):
        objekte.append({
            'pos_x': random.randint(-size, size),
            'pos_y': random.randint(-size, size),
            'type': 'cheatsheet', #spicker ist zu deutsch oder?
            'name': 'Spicker',
            'used': False
        })
    
    return objekte

def play_game():
    show_intro()
    
    # Setup
    player_name = input("Spielername: ").strip() or "Alex"
    
    print("\nSpielfeldgröße:")
    world_size = hohe_zahl_eingabe("Grenze eingeben 10-50: ", 30, 10, 50)
    
    print(f"\nStartposition x/y:")
    pos_x = hohe_zahl_eingabe("X: ", 0, -world_size, world_size)
    pos_y = hohe_zahl_eingabe("Y: ", 0, -world_size, world_size)
    
    nerven = hohe_zahl_eingabe("\nStart-Nervenkraft 10-150: ", 100, 10, 150)
    max_runden = hohe_zahl_eingabe("Rundenlimit: ", 25, 1, 100)
    
    # Game status
    aktuelle_runde = 0
    spiel_log = []
    warum_verloren = ""
    spiel_ergebniss = "Fehlgeschlagen"
    
    start_pos = (pos_x, pos_y)
    start_nerven = nerven
    
    # Welt generieren
    objects = generate_world(world_size)
    
    sekreteriat_x = random.randint(-world_size, world_size)
    sekreteriat_y = random.randint(-world_size, world_size)
    
    # Nicht direkt auf Start spawnen
    if sekreteriat_x == pos_x and sekreteriat_y == pos_y:
        sekreteriat_x += 5
    
    clear_screen()
    print("\n" + "="*55)
    print("DIE GLOCKE LÄUTET!")
    print(f"Spieler: {player_name}")
    print(f"Start: {start_pos} -> Ziel: ({sekreteriat_x}, {sekreteriat_y})")
    print(f"Nerven: {nerven} | Runden: {max_runden}")
    print("="*55 + "\n")
    input("Enter zum Starten...")
    
    # Main Loop
    while aktuelle_runde < max_runden and nerven > 0:
        aktuelle_runde += 1
        old_x, old_y = pos_x, pos_y
        old_nerves = nerven
        event_msg = "Nichts besonderes passiert."
        effekt_msg = "Bewegung kostet 8 Nerven."
        
        print(f"\n[Runde {aktuelle_runde}/{max_runden}]")
        print(f"Position: ({old_x}, {old_y}) | Nerven: {old_nerves}")
        
        # Steuerung
        aktion = input("WASD bewegen, Q aufgeben > ").upper().strip()
        
        if aktion == "Q":
            warum_verloren = "Aufgegeben."
            break
        
        schritt = 3
        if aktion == "W": pos_y += schritt
        elif aktion == "S": pos_y -= schritt
        elif aktion == "A": pos_x -= schritt
        elif aktion == "D": pos_x += schritt
        else:
            print("Ungültig! Du taumelst verwirrt rum.")
            pos_x += random.choice([-1, 1])
            pos_y += random.choice([-1, 1])
        
        nerven -= 8
        
        # Rand der Map
        if abs(pos_x) > world_size or abs(pos_y) > world_size:
            event_msg = "Brandschutztür versperrt den Weg!"
            effekt_msg = "Umdrehen kostet extra 12 Nerven."
            pos_x = max(-world_size, min(world_size, pos_x))
            pos_y = max(-world_size, min(world_size, pos_y))
            nerven -= 12
        
        # Objekte checken
        for obj in objects:
            if obj['used']: continue
            
            if abs(pos_x - obj['pos_x']) <= 3 and abs(pos_y - obj['pos_y']) <= 3:
                if obj['type'] == 'kiosk':
                    nerven += 25
                    event_msg = f"{obj['name']} gefunden bei ({obj['pos_x']}, {obj['pos_y']})"
                    effekt_msg = "Energy Drink! +25 Nerven"
                    spiel_log.append(f"Runde {aktuelle_runde}: Kiosk entdeckt")
                    obj['used'] = True
                
                elif obj['type'] == 'janitor':
                    nerven -= 20
                    event_msg = f"{obj['name']} erwischt dich!"
                    effekt_msg = "'Nicht rennen!' -20 Nerven"
                    spiel_log.append(f"Runde {aktuelle_runde}: Ärger mit Hausmeister")
                    obj['used'] = True
                
                elif obj['type'] == 'cheatsheet':
                    nerven += 10
                    event_msg = f"Geheimes {obj['name']} gefunden!"
                    effekt_msg = "Sicherheitsgefühl +10 Nerven"
                    spiel_log.append(f"Runde {aktuelle_runde}: Spicker gefunden")
                    obj['used'] = True
        
        # Zufallsereignis 20% - villeicht auf 30 oder 40 erhöhen?. es ist sonst etwas langweilig
        if random.random() < 0.2:
            if random.choice([True, False]):
                nerven -= 15
                event_msg = "Pop-Quiz! Lehrer zieht dich rein!"
                effekt_msg = "Schock -15 Nerven"
            else:
                pos_x += random.randint(-5, 5)
                pos_y += random.randint(-5, 5)
                event_msg = "Pausengedränge!"
                effekt_msg = "Wirst durch die Gegend geschubst"
        
        # Sieg?
        if abs(pos_x - sekreteriat_x) <= 2 and abs(pos_y - sekreteriat_y) <= 2:
            warum_verloren = "Sekretariat erreicht! Dokument abgegeben!"
            spiel_ergebniss = "Erfolg!"
            break
        
        # Status
        print(f"-> Neue Position: ({pos_x}, {pos_y})")
        print(f"-> Nerven: {nerven}")
        print(f"-> Event: {event_msg}")
        print(f"-> Effekt: {effekt_msg}")
        print("-" * 50)
    
    # Ende auswerten
    if not warum_verloren:
        if nerven <= 0:
            warum_verloren = "Nerven aufgebraucht. Zusammenbruch auf Toilette."
            spiel_ergebniss = "Fehlgeschlagen"
        else:
            warum_verloren = "Zeit abgelaufen. Glocke läutet."
            spiel_ergebniss = "Teilerfolg"
    
    # Abschluss
    print("\n" + "="*60)
    print("                        MISSIONSBERICHT")
    print("="*60)
    print(f"Name: {player_name}")
    print(f"Start: {start_pos} mit {start_nerven} Nerven")
    print(f"Ende: ({pos_x}, {pos_y}) | Ziel war ({sekreteriat_x}, {sekreteriat_y})")
    print(f"Runden: {aktuelle_runde}/{max_runden}")
    print(f"Nerven übrig: {max(0, nerven)}") # max(0...) verhindert Minuszahlen im Bericht
    print(f"Ergebnis: {spiel_ergebniss}")
    print(f"Grund: {warum_verloren}")
    print("-" * 60)
    print("Wichtige Ereignisse:")
    if spiel_log:
        for evt in spiel_log:
            print(f"  • {evt}")
    else:
        print("  • Keine besonderen Vorkommnisse")
    print("="*60 + "\n")

def main():
    while True:
        play_game()
        again = input("Nächste Runde? ja/nein: ").lower().strip()
        if again not in ['ja', 'j', 'yes', 'y']:
            print("\n" + "="*50)
            print("Danke fürs Spielen!")
            print("Eingereicht von: Hannes Meinen | Gigathon 2026")
            print("="*50)
            break
        clear_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSpiel abgebrochen. Bis nächstes Mal!")
        sys.exit(0)