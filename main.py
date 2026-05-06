import database_tris as db

def stampa_scacchiera(s):
    visiva = [str(i + 1) if s[i] == "_" else s[i] for i in range(9)]
    print("\n")
    print(f" {visiva[0]} | {visiva[1]} | {visiva[2]} ")
    print("-----------")
    print(f" {visiva[3]} | {visiva[4]} | {visiva[5]} ")
    print("-----------")
    print(f" {visiva[6]} | {visiva[7]} | {visiva[8]} ")
    print("\n")

def fai_mossa(scacchiera, posizione, giocatore):
    indice = posizione - 1
    if 0 <= indice <= 8 and scacchiera[indice] == "_":
        scacchiera[indice] = giocatore
        return True
    return False

def ha_vinto(scacchiera, giocatore):
    combinazioni = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for c in combinazioni:
        if scacchiera[c[0]] == scacchiera[c[1]] == scacchiera[c[2]] == giocatore:
            return True
    return False

# QUESTA È LA NUOVA FUNZIONE PER IL DATABASE
def ottieni_o_crea_giocatore(nome):
    # Controlla se esiste
    query_select = "SELECT id_giocatore FROM giocatori WHERE nome = %s"
    risultato = db.esegui_select(query_select, (nome,))
    
    if risultato:
        return risultato[0]['id_giocatore']
    else:
        # Se non esiste lo crea
        query_insert = "INSERT INTO giocatori (nome) VALUES (%s)"
        db.esegui_dml(query_insert, (nome,))
        # Recupera l'id appena creato
        nuovo_risultato = db.esegui_select(query_select, (nome,))
        return nuovo_risultato[0]['id_giocatore']


def salva_risultato_partita(id_g1, id_g2, id_vincitore, esito):
    query = """
        INSERT INTO partite (id_giocatore1, id_giocatore2, id_vincitore, esito) 
        VALUES (%s, %s, %s, %s)
    """
    # id_vincitore sarà l'ID di chi ha vinto, oppure None se è pareggio
    db.esegui_dml(query, (id_g1, id_g2, id_vincitore, esito))
    print("Risultato della partita salvato nel database!")

def mostra_classifica():
    query = """
        SELECT giocatori.nome, COUNT(partite.id_vincitore) AS vittorie
        FROM giocatori
        JOIN partite ON giocatori.id_giocatore = partite.id_vincitore
        WHERE partite.esito = 'vittoria'
        GROUP BY giocatori.id_giocatore
        ORDER BY vittorie DESC
        LIMIT 5
    """
    classifica = db.esegui_select(query)
    print("\n--- CLASSIFICA TOP 5 ---")
    for i, riga in enumerate(classifica, 1):
        print(f"{i}. {riga['nome']} - {riga['vittorie']} vittorie")
    print("------------------------\n")

def mostra_statistiche_giocatore(nome):
    # Recuperiamo l'ID del giocatore
    query_id = "SELECT id_giocatore FROM giocatori WHERE nome = %s"
    res = db.esegui_select(query_id, (nome,))
    
    if not res:
        print("Giocatore non trovato.")
        return

    id_g = res[0]['id_giocatore']

    # Contiamo quante ne ha giocate (come G1 o come G2)
    query_giocate = "SELECT COUNT(*) AS total FROM partite WHERE id_giocatore1 = %s OR id_giocatore2 = %s"
    giocate = db.esegui_select(query_giocate, (id_g, id_g))[0]['total']

    # Contiamo quante ne ha vinte
    query_vinte = "SELECT COUNT(*) AS v FROM partite WHERE id_vincitore = %s"
    vinte = db.esegui_select(query_vinte, (id_g,))[0]['v']

    # Contiamo i pareggi
    query_pareggi = "SELECT COUNT(*) AS p FROM partite WHERE (id_giocatore1 = %s OR id_giocatore2 = %s) AND esito = 'pareggio'"
    pareggi = db.esegui_select(query_pareggi, (id_g, id_g))[0]['p']

    perse = giocate - vinte - pareggi
    win_rate = (vinte / giocate * 100) if giocate > 0 else 0

    print(f"\n--- STATISTICHE DI {nome} ---")
    print(f"Partite giocate: {giocate}")
    print(f"Vinte: {vinte}")
    print(f"Perse: {perse}")
    print(f"Pareggi: {pareggi}")
    print(f"Win Rate: {win_rate:.1f}%")
    print("----------------------------\n")

def gioca():
    # 1. IDENTIFICAZIONE GIOCATORI
    nome1 = input("Inserisci nome Giocatore 1 (X): ")
    id1 = ottieni_o_crea_giocatore(nome1)
    
    nome2 = input("Inserisci nome Giocatore 2 (O): ")
    id2 = ottieni_o_crea_giocatore(nome2)

    scacchiera = ["_"] * 9
    giocatore_corrente = "X"
    id_corrente = id1
    mosse_fatte = 0

    while True:
        stampa_scacchiera(scacchiera)
        
        # Turno del giocatore
        while True:
            scelta = input(f"Turno di {giocatore_corrente}. Scegli posizione (1-9): ")
            try:
                scelta = int(scelta)
                if 1 <= scelta <= 9 and fai_mossa(scacchiera, scelta, giocatore_corrente):
                    break
                else:
                    print("Mossa non valida o cella occupata.")
            except ValueError:
                print("Inserisci un numero!")

        mosse_fatte += 1

        # Controllo Vittoria
        if ha_vinto(scacchiera, giocatore_corrente):
            stampa_scacchiera(scacchiera)
            print(f"Vittoria {giocatore_corrente}")
            salva_risultato_partita(id1, id2, id_corrente, 'vittoria')
            break

        if mosse_fatte == 9:
            stampa_scacchiera(scacchiera)
            print("Pareggio")
            salva_risultato_partita(id1, id2, None, 'pareggio')
            break

        # Cambio turno
        if giocatore_corrente == "X":
            giocatore_corrente = "O"
            id_corrente = id2
        else:
            giocatore_corrente = "X"
            id_corrente = id1

if __name__ == "__main__":
    while True:
        print("Menu")
        print("1. Nuova Partita")
        print("2. Visualizza la Top 5")
        print("3. Statistiche Giocatore")
        print("4. Esci")
        
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            gioca()
        elif scelta == "2":
            mostra_classifica()
        elif scelta == "3":
            nome_cercato = input("Di quale giocatore vuoi vedere le statistiche? ")
            mostra_statistiche_giocatore(nome_cercato)
        elif scelta == "4":
            print("fine")
            break
        else:
            print("Opzione non valida.")
