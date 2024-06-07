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
from APP_FILMS_164.Suivi.gestion_suivi_wtf_forms import FormWTFAjouterSuivi
from APP_FILMS_164.Suivi.gestion_suivi_wtf_forms import FormWTFDeleteSuivi
from APP_FILMS_164.Suivi.gestion_suivi_wtf_forms import FormWTFUpdateSuivi

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /suivi_afficher
    
    Test : ex : http://127.0.0.1:5575/suivi_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_suivi_sel = 0 >> tous les genres.
                id_suivi_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/suivi/suivi_afficher/<string:order_by>/<int:id_suivi_sel>", methods=['GET', 'POST'])
def suivi_afficher(order_by, id_suivi_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_suivi_sel == 0:
                    strsql_suivi_afficher = """SELECT t_suivi.id_suivi, t_suivi.annee, t_matiere.nom_matiere, t_apprenti.nom_apprenti
                                                FROM t_suivi
                                                JOIN t_matiere ON t_suivi.fk_matiere = t_matiere.id_matiere
                                                JOIN t_apprenti ON t_suivi.fk_apprenti = t_apprenti.id_apprennti;
                                            """
                    mc_afficher.execute(strsql_suivi_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_suivi_selected": id_suivi_sel}
                    strsql_genres_afficher = """SELECT * FROM t_suivi WHERE id_suivi = %(value_id_suivi_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_suivi_afficher = """SELECT * FROM t_suivi ORDER BY id_suivi DESC"""

                    mc_afficher.execute(strsql_suivi_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_suivi_sel == 0:
                    flash("""La table "t_suivi" est vide. !!""", "warning")
                elif not data_genres and id_suivi_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le suivi demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données suivi affichés !!", "success")

        except Exception as Exception_suivi_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{suivi_afficher.__name__} ; "
                                          f"{Exception_suivi_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("/suivi/suivi_afficher.html", data=data_genres)


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


@app.route("/suivi/suivi_ajouter", methods=['GET', 'POST'])
def suivi_ajouter_wtf():
    form = FormWTFAjouterSuivi()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                fk_matiere_wtf = form.fk_matiere_wtf.data
                fk_apprenti_wtf = form.fk_apprenti_wtf.data
                annee_wtf = form.annee_wtf.data
                valeurs_insertion_dictionnaire = {
                                                  "value_fk_matiere": fk_matiere_wtf,
                                                  "value_fk_apprenti": fk_apprenti_wtf,
                                                  "value_annee": annee_wtf,
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_suivi (id_suivi, fk_matiere, fk_apprenti, annee) 
                         VALUES (NULL, %(value_fk_matiere)s, %(value_fk_apprenti)s, %(value_annee)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('suivi_afficher', order_by='DESC', id_suivi_sel=0))

        except Exception as Exception_suivi_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{suivi_ajouter_wtf.__name__} ; "
                                            f"{Exception_suivi_ajouter_wtf}")

    return render_template("/suivi/suivi_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /suivi_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "suivi_afficher.html"
    
    Remarque :  Dans le champ "nom_suivi_update_wtf" du formulaire "genres/suivi_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/suivi_update", methods=['GET', 'POST'])
def suivi_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_suivi_update = request.values['id_suivi_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateSuivi()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupérer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            fk_apprenti_update = form_update.fk_apprenti_update_wtf.data
            fk_matiere_update = form_update.fk_matiere_update_wtf.data
            annee_update = form_update.annee_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_suivi": id_suivi_update,
                "value_fk_apprenti": fk_apprenti_update,
                "value_fk_matiere": fk_matiere_update,
                "value_annee": annee_update,
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """
                UPDATE t_suivi
                SET fk_apprenti = %(value_fk_apprenti)s, 
                    fk_matiere = %(value_fk_apprenti)s, 
                    annee = %(value_annee)s
                WHERE id_suivi = %(value_id_suivi)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('suivi_afficher', order_by="ASC", id_suivi_sel=id_suivi_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_suivi = """
                SELECT *
                FROM t_suivi
                WHERE id_suivi = %(value_id_suivi)s
            """
            valeur_select_dictionnaire = {"value_id_suivi": id_suivi_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_suivi, valeur_select_dictionnaire)
                data_annee = mybd_conn.fetchone()

            print("data_annee ", data_annee, " type ", type(data_annee), " annee ",
                  data_annee["annee"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"
            form_update.fk_apprenti_update_wtf.data = data_annee["fk_apprenti"]
            form_update.fk_matiere_update_wtf.data = data_annee["fk_matiere"]
            form_update.annee_update_wtf.data = data_annee["annee"]


    except Exception as e:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  {suivi_update_wtf.__name__} ; {e}")

    return render_template("Suivi/suivi_update_wtf.html", form_update=form_update)




"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "suivi_afficher.html"
    
    Remarque :  Dans le champ "nom_suivi_delete_wtf" du formulaire "genres/suivi_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/suivi/suivi_delete", methods=['GET', 'POST'])
def suivi_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    id_genre_delete = request.values.get('id_suivi_btn_delete_html')

    form_delete = FormWTFDeleteSuivi()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("suivi_afficher", order_by="ASC", id_suivi_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_films_attribue_genre_delete = session.get('data_films_attribue_genre_delete')
                if data_films_attribue_genre_delete is None:
                    print("Erreur : 'data_films_attribue_genre_delete' n'est pas dans la session")
                    flash("Erreur : données non trouvées dans la session", "danger")
                    return redirect(url_for("suivi_afficher", order_by="ASC", id_suivi_sel=0))

                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)
                flash(f"Effacer le suivi de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_suivi": id_genre_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """DELETE FROM t_suivi WHERE id_suivi = %(value_id_suivi)s"""
                str_sql_delete_idgenre = """DELETE FROM t_suivi WHERE id_suivi = %(value_id_suivi)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")
                return redirect(url_for('suivi_afficher', order_by="ASC", id_suivi_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_suivi": id_genre_delete}
            print(id_genre_delete, type(id_genre_delete))

            str_sql_genres_films_delete = """SELECT t_suivi.id_suivi, t_suivi.annee, t_matiere.nom_matiere, t_apprenti.nom_apprenti
                                                FROM t_suivi
                                                JOIN t_matiere ON t_suivi.fk_matiere = t_matiere.id_matiere
                                                JOIN t_apprenti ON t_suivi.fk_apprenti = t_apprenti.id_apprennti;"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                str_sql_id_genre = """SELECT t_suivi.id_suivi, t_suivi.annee, t_matiere.nom_matiere, t_apprenti.nom_apprenti
                                                FROM t_suivi
                                                JOIN t_matiere ON t_suivi.fk_matiere = t_matiere.id_matiere
                                                JOIN t_apprenti ON t_suivi.fk_apprenti = t_apprenti.id_apprennti;"""

                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre))

                if data_nom_genre and 'suivi' in data_nom_genre:
                    form_delete.suivi_delete_wtf.data = data_nom_genre["suivi"]
                else:
                    print("Clé 'suivi' non trouvée dans data_nom_genre")
                    flash("Erreur : 'suivi' non trouvé dans les données", "danger")

            btn_submit_del = False

    except Exception as Exception_suivi_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{suivi_delete_wtf.__name__} ; "
                                      f"{Exception_suivi_delete_wtf}")

    return render_template("/suivi/suivi_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)





