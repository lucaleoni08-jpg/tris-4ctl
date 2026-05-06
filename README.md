# Progetto Tris con Database SQL

## Descrizione del Progetto
Questo progetto consiste in un classico gioco del tris sviluppato in Python in un sistema completo capace di memorizzare lo storico delle partite su un database MySQL. 
Il programma permette di sfidare un altro giocatore, salvare i risultati in tempo reale e visualizzare alcune statistiche come la Top 5 dei giocatori e lo storico delle vittorie per ciascun gioccatore.

## Funzionalità
- Gestione Giocatori: Registrazione automatica dei nuovi utenti nel database.
- Logica di Gioco: E' un semplice 1 contro 1 ma situato nel terminale.
- Persistenza Dati: Ogni partita è salvata con i relativi partecipanti, con la data,l'ora e l'esito finale.
- Statistiche: Classifica dei primi 5 giocatori per numero di vittorie.
- Statistiche dettagliate per ogni giocatore (giocate, vinte, perse, win rate).

## Requisiti Tecnici
- Linguaggio: Python 3
- Librerie: `pymysql`
- Database: MySQL / MariaDB
- Connessione: Tunnel SSH sulla porta 3307 tramite il file usato nel progetto precedente(conn3)

## Organizzazione del Gruppo
Il progetto è stato realizzato da:
1. [LeoniLuca]: Responsabile database, connessione Python-SQL e gestione tabelle.
2. [DesantisThomas]: Responsabile logica di gioco (Tris) e integrazione menu.
3. [TaglianiRocco]: Responsabile statistiche, query SQL avanzate e documentazione.

## Istruzioni per l'installazione
1. Clonare il repository.
2. Eseguire lo script SQL contenuto in `schema.sql` su phpMyAdmin.
3. Aprire il tunnel SSH tramite il comando:
  
   ssh -N -L 3307:localhost:3306 [utente]@lab.alberghetti.cloud

   IMPORTANTE:Il nome utente non deve includere il prefisso 4CTL_

5. Avviare il gioco:
  python main.py
