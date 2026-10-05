from rich import print as rprint
from rich.console import Console
from rich.table import Table

import sqlite3
con = sqlite3.connect("todolist.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS Tache(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nom TEXT NOT NULL, 
        etat BOOLEAN NOT NULL DEFAULT 0
    )
""")


taches = []
taches_a_faire = []
# cur.executemany("INSERT INTO Tache (nom) VALUES(?)", taches)
# con.commit()

res = cur.execute("SELECT nom FROM Tache")
row = res.fetchone()
while(row is not None):
    taches.append(row[0])
    row = res.fetchone()
print(taches)

res = cur.execute("SELECT nom FROM Tache where etat = 1")
finies = set()
row = res.fetchone()
while(row is not None):
    finies.add(row[0])
    row = res.fetchone()
print(finies)


programme_en_cours = True

def attendreSortieUtilisateur():
    rprint("Appuie sur entrée pour sortir[blink]...[/blink]")
    input()

def finirTacheBDD(str):
    cur.execute(f"UPDATE Tache set etat = 1 where nom = \"{str}\"")
    con.commit()

def ajoutTacheBDD(tache):
    cur.execute(f"INSERT INTO Tache (nom) VALUES (\"{tache}\")")
    con.commit()

def enlever():    
    taches_a_faire = list(set(taches) - finies)
    rprint("[yellow]Liste des choses à faire :[/yellow]")
    console = Console()
    table = Table()
    table.add_column("Numero", style="cyan")
    table.add_column("Nom", style="green")
    for index, value in enumerate(taches_a_faire, start=1):
        table.add_row(str(index), str(value))
    table.add_row(str(0), "Annuler", style="bold red")
    console.print(table)   
    if(len(taches_a_faire) > 0):
        choix = int(input("Selectionnez une tache terminée : ")) - 1 
        if(choix == -1):
            rprint("Annulation en cours...")
        else:
            finies.add(taches_a_faire[choix])
            finirTacheBDD(taches_a_faire[choix])
            print(f"La tache \"{taches_a_faire[choix]}\" est terminée !!!! \n ")
    else:
        rprint("[green]Aucune tache restante !![/green]")
    attendreSortieUtilisateur()

def afficher_taches_a_faire():
    taches_a_faire = list(set(taches) - finies)
    if(len(taches_a_faire) > 0):
        console = Console()
        table = Table(title="Taches à faire")
        table.add_column("Numero", style="cyan", justify="right")
        table.add_column("Nom", style="green")

        for index, i in enumerate(taches_a_faire):
            table.add_row(str(index), str(i))
        console.print(table)
        print("\n")
    else:
        rprint("[green]Aucune tache restante !![/green]")
    attendreSortieUtilisateur()

def afficher_taches():
    console = Console()
    table = Table(title="Toutes les taches")
    table.add_column("Numero", style="cyan", justify="right")
    table.add_column("Nom", style="green")
    table.add_column("Etat", style="red")
    for index, i in enumerate(taches):
        etat = "En cours"
        if i in finies:
            etat = "Terminée"
        table.add_row(str(index), str(i), etat)
    console.print(table)
    print("\n")
    attendreSortieUtilisateur()

def afficher_taches_finies():
    if(len(finies) > 0):
        console = Console()
        table = Table(title="Taches finies")
        table.add_column("Numero", style="cyan", justify="right")
        table.add_column("Nom", style="green")
        for index, i in enumerate(finies):
            table.add_row(str(index), str(i))
        console.print(table)
    else:
        print("Aucune tache finie")
    attendreSortieUtilisateur()

def ajouter():
    rprint("Quelle tache voulez-vous ajouter ? [italic red]!q[/italic red] pour annuler\n")
    tache = input()
    if(tache != "!q"):
        taches.append(tache)
        ajoutTacheBDD(tache)
        rprint(f"La tache \"{tache}\" a bien été ajouté à la liste !")
    else:
        rprint("Annulation en cours...")
    attendreSortieUtilisateur()

def main(programme_en_cours):
    while(programme_en_cours):
        rprint("[bold red]Que voulez-vous faire ? :[/bold red] ")
        rprint("[magenta]1[/magenta] : Finir une taches de la TODOLIST")
        rprint("[magenta]2[/magenta] : Voir la liste des taches de la TODOLIST") 
        rprint("[magenta]3[/magenta] : Ajouter une tache dans la TODOLIST") 
        rprint("[magenta]0[/magenta] : QUITTER")
        action = None
        try:
            action = int(input())
        except ValueError:
            rprint("Entrez un entier entre 0 et 3")

        match action:
            case 1:
                enlever()
            case 2:
                afficher = True
                while(afficher):
                    rprint("[bold blue]Vous voulez afficher : [/bold blue]")
                    rprint("[magenta]1[/magenta] : Les taches à faire")
                    rprint("[magenta]2[/magenta] : Toutes les taches")
                    rprint("[magenta]3[/magenta] : les taches finies")
                    rprint("[magenta]0[/magenta] : Sortir")
                    afficher = int(input())
                    match afficher:
                        case 1:
                            afficher_taches_a_faire()
                        case 2:
                            afficher_taches()
                        case 3: 
                            afficher_taches_finies()
                        case 0:
                            afficher = False
            case 3:
                ajouter()
            case 0:
                programme_en_cours = False
            case _:
                rprint("Entrez un nombre valide")

if __name__ == "__main__":
    main(programme_en_cours)