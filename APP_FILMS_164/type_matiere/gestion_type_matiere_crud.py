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
from APP_FILMS_164.type_matiere.gestion_type_matiere_wtf_forms import FormWTFAjouterTypeMatiere
from APP_FILMS_164.type_matiere.gestion_type_matiere_wtf_forms import FormWTFDeleteTypeMatiere
from APP_FILMS_164.type_matiere.gestion_type_matiere_wtf_forms import FormWTFUpdateTypeMatiere

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /matiere_afficher
    
    Test : ex : http://127.0.0.1:5575/matiere_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_matiere_sel = 0 >> tous les genres.
                id_matiere_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/type_matiere/type_matiere_afficher/<string:order_by>/<int:id_type_matiere_sel>", methods=['GET', 'POST'])
def type_matiere_afficher(order_by, id_type_matiere_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_type_matiere_sel == 0:
                    strsql_type_matiere_afficher = """SELECT * FROM t_type_matiere"""
                    mc_afficher.execute(strsql_type_matiere_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_type_matiere_selected": id_type_matiere_sel}
                    strsql_genres_afficher = """SELECT * FROM t_type_matiere WHERE id_type_matiere = %(value_id_type_matiere_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_type_matiere_afficher = """SELECT * FROM t_type_matiere ORDER BY id_type_matiere DESC"""

                    mc_afficher.execute(strsql_type_matiere_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_type_matiere_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_genres and id_type_matiere_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données genres affichés !!", "success")

        except Exception as Exception_type_matiere_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{type_matiere_afficher.__name__} ; "
                                          f"{Exception_type_matiere_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("/type_matiere/type_matiere_afficher.html", data=data_genres)


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


@app.route("/type_matiere/type_matiere_ajouter", methods=['GET', 'POST'])
def type_matiere_ajouter_wtf():
    form = FormWTFAjouterTypeMatiere()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                type_matiere_wtf = form.type_matiere_wtf.data
                valeurs_insertion_dictionnaire = {"value_type_matiere": type_matiere_wtf}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_type_matiere (id_type_matiere, type_matiere) 
                         VALUES (NULL, %(value_type_matiere)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('type_matiere_afficher', order_by='DESC', id_type_matiere_sel=0))

        except Exception as Exception_type_matiere_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{type_matiere_ajouter_wtf.__name__} ; "
                                            f"{Exception_type_matiere_ajouter_wtf}")

    return render_template("/type_matiere/type_matiere_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /type_matiere_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "type_matiere_afficher.html"
    
    Remarque :  Dans le champ "nom_type_matiere_update_wtf" du formulaire "genres/type_matiere_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/type_matiere/type_matiere_update", methods=['GET', 'POST'])
def type_matiere_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_type_matiere_update = request.values['id_type_matiere_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateTypeMatiere()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupérer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            type_matiere_update = form_update.type_matiere_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_type_matiere": id_type_matiere_update,
                "value_type_matiere": type_matiere_update,
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """
                UPDATE t_type_matiere
                SET type_matiere = %(value_type_matiere)s
                WHERE id_type_matiere = %(value_id_type_matiere)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('type_matiere_afficher', order_by="ASC", id_type_matiere_sel=id_type_matiere_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_type_matiere = """
                SELECT *
                FROM t_type_matiere
                WHERE id_type_matiere = %(value_id_type_matiere)s
            """
            valeur_select_dictionnaire = {"value_id_type_matiere": id_type_matiere_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_type_matiere, valeur_select_dictionnaire)
                data_type_matiere = mybd_conn.fetchone()

            print("data_type_matiere ", data_type_matiere, " type ", type(data_type_matiere), " type_matiere ",
                  data_type_matiere["type_matiere"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"
            form_update.type_matiere_update_wtf.data = data_type_matiere["type_matiere"]


    except Exception as e:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  {type_matiere_update_wtf.__name__} ; {e}")

    return render_template("type_matiere/type_matiere_update_wtf.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "matiere_afficher.html"
    
    Remarque :  Dans le champ "nom_matiere_delete_wtf" du formulaire "matiere/matiere_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/type_matiere/type_matiere_delete", methods=['GET', 'POST'])
def type_matiere_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_type_matiere_delete = request.values.get('id_type_matiere_btn_delete_html')

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteTypeMatiere()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("type_matiere_afficher", order_by="ASC", id_type_matiere_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/matiere_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session.get('data_films_attribue_genre_delete')
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_type_matiere": id_type_matiere_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """DELETE FROM t_type_matiere WHERE id_type_matiere = %(value_id_type_matiere)s"""
                str_sql_delete_idgenre = """DELETE FROM t_type_matiere WHERE id_type_matiere = %(value_id_type_matiere)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('type_matiere_afficher', order_by="ASC", id_type_matiere_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_type_matiere": id_type_matiere_delete}
            print(id_type_matiere_delete, type(id_type_matiere_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT * FROM t_type_matiere"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/matiere_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_genre =  """SELECT * FROM t_type_matiere"""

                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["type_matiere"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "matiere_delete_wtf.html"
            form_delete.type_matiere_delete_wtf.data = data_nom_genre["type_matiere"]

            # Le bouton pour l'action "DELETE" dans le form. "nom_matiere_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_type_matiere_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{type_matiere_delete_wtf.__name__} ; "
                                      f"{Exception_type_matiere_delete_wtf}")

    return render_template("/type_matiere/type_matiere_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)




