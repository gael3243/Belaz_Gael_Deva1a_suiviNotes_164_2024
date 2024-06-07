"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.notes.gestion_notes_wtf_forms import FormWTFAjouterNotes
from APP_FILMS_164.notes.gestion_notes_wtf_forms import FormWTFDeleteNotes
from APP_FILMS_164.notes.gestion_notes_wtf_forms import FormWTFUpdateNotes

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /notes_afficher
    
    Test : ex : http://127.0.0.1:5575/notes_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_notes_sel = 0 >> tous les genres.
                id_notes_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/notes/notes_afficher/<string:order_by>/<int:id_notes_sel>", methods=['GET', 'POST'])
def notes_afficher(order_by, id_notes_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_notes_sel == 0:
                    strsql_notes_afficher = """SELECT tn.id_notes, tn.notes, tm.nom_matiere, ttn.type_notes, ta.nom_apprenti
                                                    FROM t_notes tn
                                                    INNER JOIN t_matiere tm ON tn.fk_matiere = tm.id_matiere
                                                    INNER JOIN t_type_notes ttn ON tn.fk_typeNotes = ttn.id_type_notes
                                                    INNER JOIN t_apprenti ta ON tn.fk_apprenti = ta.id_apprennti;
                                                """
                    mc_afficher.execute(strsql_notes_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_notes_selected": id_notes_sel}
                    strsql_genres_afficher = """SELECT * FROM t_notes WHERE id_notes = %(value_id_notes_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_notes_afficher = """SELECT * FROM t_notes ORDER BY id_notes DESC"""

                    mc_afficher.execute(strsql_notes_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_notes_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_genres and id_notes_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données genres affichés !!", "success")

        except Exception as Exception_notes_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{notes_afficher.__name__} ; "
                                          f"{Exception_notes_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("/notes/notes_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/notes/notes_ajouter", methods=['GET', 'POST'])
def notes_ajouter_wtf():
    form = FormWTFAjouterNotes()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                notes_wtf = form.notes_wtf.data
                fk_matiere_wtf = form.fk_matiere_wtf.data
                fk_typeNotes_wtf = form.fk_typeNotes_wtf.data
                fk_apprenti_wtf = form.fk_apprenti_wtf.data
                valeurs_insertion_dictionnaire = {"value_notes": notes_wtf,
                                                  "value_fk_matiere": fk_matiere_wtf,
                                                  "value_fk_typeNotes": fk_typeNotes_wtf,
                                                  "value_fk_apprenti": fk_apprenti_wtf,
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_notes (id_notes, notes, fk_matiere, fk_typeNotes, fk_apprenti) 
                         VALUES (NULL, %(value_notes)s, %(value_fk_matiere)s, %(value_fk_typeNotes)s, %(value_fk_apprenti)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('notes_afficher', order_by='DESC', id_notes_sel=0))

        except Exception as Exception_notes_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{notes_ajouter_wtf.__name__} ; "
                                            f"{Exception_notes_ajouter_wtf}")

    return render_template("/notes/notes_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /notes_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "notes_afficher.html"
    
    Remarque :  Dans le champ "nom_notes_update_wtf" du formulaire "genres/notes_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/notes_update", methods=['GET', 'POST'])
def notes_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_notes_update = request.values['id_notes_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateNotes()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupérer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            notes_update = form_update.notes_update_wtf.data
            fk_matiere_update = form_update.fk_matiere_update_wtf.data
            fk_apprenti_update = form_update.fk_apprenti_update_wtf.data
            fk_typeNotes_update = form_update.fk_typeNotes_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_notes": id_notes_update,
                "value_notes": notes_update,
                "value_fk_apprenti": fk_apprenti_update,
                "value_fk_matiere": fk_matiere_update,
                "value_fk_typeNotes" : fk_typeNotes_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """
                UPDATE t_notes
                SET notes = %(value_notes)s,
                    fk_apprenti = %(value_fk_apprenti)s, 
                    fk_matiere = %(value_fk_matiere)s, 
                    fk_typeNotes = %(value_fk_typeNotes)s
                WHERE id_notes = %(value_id_notes)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('notes_afficher', order_by="ASC", id_notes_sel=id_notes_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_notes = """
                SELECT *
                FROM t_notes
                WHERE id_notes = %(value_id_notes)s
            """
            valeur_select_dictionnaire = {"value_id_notes": id_notes_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_notes, valeur_select_dictionnaire)
                data_notes = mybd_conn.fetchone()

            print("data_notes ", data_notes, " type ", type(data_notes), " notes ",
                  data_notes["notes"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"
            form_update.notes_update_wtf.data = data_notes["notes"]
            form_update.fk_apprenti_update_wtf.data = data_notes["fk_apprenti"]
            form_update.fk_matiere_update_wtf.data = data_notes["fk_matiere"]
            form_update.fk_typeNotes_update_wtf.data = data_notes["fk_typeNotes"]


    except Exception as e:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  {notes_update_wtf.__name__} ; {e}")

    return render_template("notes/notes_update_wtf.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "notes_afficher.html"
    
    Remarque :  Dans le champ "nom_notes_delete_wtf" du formulaire "genres/notes_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/notes/notes_delete", methods=['GET', 'POST'])
def notes_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_genre_delete = request.values['id_notes_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteNotes()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("notes_afficher", order_by="ASC", id_notes_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/notes_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_genre": id_genre_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """DELETE FROM t_notes WHERE id_notes = %(value_id_genre)s"""
                str_sql_delete_idgenre = """DELETE FROM t_notes WHERE id_notes = %(value_id_genre)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('notes_afficher', order_by="ASC", id_notes_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_genre_delete}
            print(id_genre_delete, type(id_genre_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT tn.id_notes, tn.notes, tm.nom_matiere, ttn.type_notes, ta.nom_apprenti
                                                    FROM t_notes tn
                                                    INNER JOIN t_matiere tm ON tn.fk_matiere = tm.id_matiere
                                                    INNER JOIN t_type_notes ttn ON tn.fk_typeNotes = ttn.id_type_notes
                                                    INNER JOIN t_apprenti ta ON tn.fk_apprenti = ta.id_apprennti
                                                     WHERE id_notes = %(value_id_genre)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/notes_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_genre = """SELECT tn.id_notes, tn.notes, tm.nom_matiere, ttn.type_notes, ta.nom_apprenti
                                                    FROM t_notes tn
                                                    INNER JOIN t_matiere tm ON tn.fk_matiere = tm.id_matiere
                                                    INNER JOIN t_type_notes ttn ON tn.fk_typeNotes = ttn.id_type_notes
                                                    INNER JOIN t_apprenti ta ON tn.fk_apprenti = ta.id_apprennti
                                                     WHERE id_notes = %(value_id_genre)s"""

                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["notes"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "notes_delete_wtf.html"
            form_delete.notes_delete_wtf.data = data_nom_genre["notes"]

            # Le bouton pour l'action "DELETE" dans le form. "notes_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_notes_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{notes_delete_wtf.__name__} ; "
                                      f"{Exception_notes_delete_wtf}")

    return render_template("/notes/notes_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)




