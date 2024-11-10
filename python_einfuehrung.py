import sqlite3
conn = sqlite3.connect('jugendherbergen_verwaltung.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS jugendherbergen (
    JID INTEGER PRIMARY KEY, 
    name TEXT NOT NULL,
    adresse TEXT NOT NULL)''')

    
cursor.execute('''
CREATE TABLE IF NOT EXISTS zimmer (
    ZID INTEGER PRIMARY KEY, 
    bettenZahl INTEGER,
    PID INTEGER,
    JID INTEGER,
    FOREIGN KEY (JID) REFERENCES jugendherbergen(JID), 
    FOREIGN KEY (PID) REFERENCES preiskategorie(PID) 

)''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS buchung (
    BuID INTEGER PRIMARY KEY, 
    startDatum CHAR(255), 
    endDatum CHAR(255),
    ZID INTEGER,
    FOREIGN KEY (ZID) REFERENCES zimmer(ZID) 

)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS benutzer (
    BeID INTEGER PRIMARY KEY, 
    vorname TEXT,
    nachname TEXT,
    email TEXT,
    passwort TEXT,
    PID INTEGER,
    FOREIGN KEY (PID) REFERENCES preiskategorie(PID)   
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS preiskategorie (
    PID INTEGER PRIMARY KEY, 
    name TEXT,
    preis REAL
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS benutzerBuchung(
    ID INTEGER PRIMARY KEY, 
    BuID INTEGER,
    BeID INTEGER
)''')

cursor.execute("""
INSERT INTO jugendherbergen (name, adresse) 
VALUES 
('Jugendherberge Feldkirch', 'Carinagasse 15, Feldkirch'),
('Jugendherberge Bludenz', 'Bahnhofstraße 12, Bludenz'),
('Jugendherberge Bregenz', 'Römerstraße 2, Bregenz'),
('Jugendherberge Schruns', 'Bahnhofstraße 5, Schruns')
""")

cursor.execute("""
INSERT INTO preiskategorie (name, preis) 
VALUES 
('Standard', 35.00),
('Premium', 45.00),
('Deluxe', 55.00),
('Economy', 25.00)
""")

cursor.execute("""
INSERT INTO zimmer (bettenZahl, JID, PID) 
VALUES 
(6, 1, 2),  
(8, 1, 3), 
(10, 1, 4), 
(4, 1, 1), 
(6, 2, 2), 
(4, 2, 1), 
(8, 2, 3), 
(10, 2, 4), 
(6, 3, 2), 
(4, 3, 1), 
(8, 3, 3), 
(10, 3, 4), 
(6, 4, 2), 
(4, 4, 1), 
(8, 4, 3), 
(10, 4, 4),
(12, 1, 2), 
(14, 1, 3),  
(16, 1, 4),  
(18, 1, 1),  
(12, 2, 2),  
(14, 2, 3),  
(16, 2, 4),  
(18, 2, 1),  
(12, 3, 2),  
(14, 3, 3),  
(16, 3, 4),  
(18, 3, 1),  
(12, 4, 2),  
(14, 4, 3),  
(16, 4, 4),  
(18, 4, 1),  
(15, 1, 2), 
(17, 1, 3),  
(19, 1, 4),  
(21, 1, 1),  
(15, 2, 2),  
(17, 2, 3),  
(19, 2, 4),  
(21, 2, 1),  
(15, 3, 2),  
(17, 3, 3),  
(19, 3, 4),  
(21, 3, 1),  
(15, 4, 2),  
(17, 4, 3),  
(19, 4, 4),  
(21, 4, 1);
""")

cursor.execute("""
INSERT INTO benutzer (vorname, nachname, email, passwort, PID) 
VALUES 
('Simon', 'Häusle', 'simonhausl3e@gmail.com', 'sef2321', 2),
('Maximilian', 'Kübler', 'kübler.max@vcon.at', '1234ers', 3),
('Katarzyna', 'Adanczyk', 'katarzyna.adanczyk@wp.pl', '!?katiczyk294', 4),
('Elias', 'Mantler', 'elias.mantler@gmail.com', 'eliMantler3hBrgz!', 1);
""")

cursor.execute("""
INSERT INTO buchung (startDatum, endDatum, ZID) 
VALUES 
('2024-11-10', '2024-11-15',1),
('2024-12-05', '2024-12-12',3),
('2024-10-12', '2024-10-16',5),
('2025-01-01', '2025-02-04',6)
""")

cursor.execute("""
INSERT INTO benutzerBuchung (BuID, BeID) 
VALUES 
(1, 1), 
(2, 2), 
(3, 3), 
(4, 4)
""")

res = cursor.execute("SELECT * FROM jugendherbergen")
print("Jugendherbergen:", list(res))

res = cursor.execute("SELECT * FROM zimmer")
print("Zimmer:", list(res))

res = cursor.execute("SELECT * FROM benutzer")
print("Benutzer:", list(res))

res = cursor.execute("SELECT * FROM buchung")
print("Buchung:", list(res))

cursor.execute('''
CREATE VIEW IF NOT EXISTS view_raumINJugendherberge AS
SELECT 
    zimmer.ZID, 
    zimmer.bettenZahl, 
    jugendherbergen.name AS jugendherberge_name,
    preiskategorie.name AS preiskategorie_name, 
    preiskategorie.preis
FROM 
    zimmer
JOIN 
    jugendherbergen ON zimmer.JID = jugendherbergen.JID
JOIN 
    preiskategorie ON zimmer.PID = preiskategorie.PID;
''')

cursor.execute('''
CREATE VIEW IF NOT EXISTS view_buchungRaumUNDBenutzer AS
SELECT 
    buchung.BuID, 
    benutzer.vorname || ' ' || benutzer.nachname AS benutzer_name,
    jugendherbergen.name AS jugendherberge_name,
    zimmer.bettenZahl,
    preiskategorie.name AS preiskategorie_name,
    buchung.startDatum,
    buchung.endDatum
FROM 
    buchung
JOIN 
    benutzerBuchung ON buchung.BuID = benutzerBuchung.BuID
JOIN 
    benutzer ON benutzerBuchung.BeID = benutzer.BeID
JOIN 
    zimmer ON buchung.ZID = zimmer.ZID
JOIN 
    jugendherbergen ON zimmer.JID = jugendherbergen.JID
JOIN 
    preiskategorie ON zimmer.PID = preiskategorie.PID;
''')

cursor.execute('''
CREATE VIEW IF NOT EXISTS view_benutzerBuchung AS
SELECT 
    benutzer.vorname || ' ' || benutzer.nachname AS benutzer_name,
    benutzer.email,
    buchung.startDatum,
    buchung.endDatum,
    jugendherbergen.name AS jugendherberge_name,
    zimmer.bettenZahl
FROM 
    benutzer
JOIN 
    benutzerBuchung ON benutzer.BeID = benutzerBuchung.BeID
JOIN 
    buchung ON benutzerBuchung.BuID = buchung.BuID
JOIN 
    zimmer ON buchung.ZID = zimmer.ZID
JOIN 
    jugendherbergen ON zimmer.JID = jugendherbergen.JID;
''')

cursor.execute('''
CREATE VIEW IF NOT EXISTS view_verfugbareRaume AS
SELECT 
    zimmer.ZID,
    zimmer.bettenZahl, 
    jugendherbergen.name AS jugendherberge_name,
    preiskategorie.name AS preiskategorie_name,
    preiskategorie.preis
FROM 
    zimmer
JOIN 
    jugendherbergen ON zimmer.JID = jugendherbergen.JID
JOIN 
    preiskategorie ON zimmer.PID = preiskategorie.PID
WHERE 
    zimmer.ZID NOT IN (
        SELECT buchung.ZID
        FROM buchung
        WHERE 
            (buchung.startDatum BETWEEN '2024-01-01' AND '2024-12-31') 
            OR 
            (buchung.endDatum BETWEEN '2024-01-01' AND '2024-12-31')
    );
''')

conn.commit()
conn.close
