from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired

class FormWTFAjouterGenres(FlaskForm):
    nom_apprenti_wtf = StringField("Nom", validators=[DataRequired(), Length(min=2, max=50), Regexp(r"^[A-Za-z\s\-]+$", message="Caractères alphabétiques uniquement")])
    prenom_apprenti_wtf = StringField("Prénom", validators=[DataRequired(), Length(min=2, max=50), Regexp(r"^[A-Za-z\s\-]+$", message="Caractères alphabétiques uniquement")])
    filiere_apprenti_wtf = StringField("Filière", validators=[DataRequired(), Length(min=2, max=50)])
    ordonance_apprenti_wtf = StringField("Ordonnance", validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField("Ajouter")

class FormWTFUpdateGenre(FlaskForm):
    nom_apprenti_update_wtf = StringField("Nom", validators=[DataRequired(), Length(min=2, max=50), Regexp(r"^[A-Za-z\s\-]+$", message="Caractères alphabétiques uniquement")])
    prenom_apprenti_update_wtf = StringField("Prénom", validators=[DataRequired(), Length(min=2, max=50), Regexp(r"^[A-Za-z\s\-]+$", message="Caractères alphabétiques uniquement")])
    filiere_apprenti_update_wtf = StringField("Filière", validators=[DataRequired(), Length(min=2, max=50)])
    ordonance_apprenti_update_wtf = StringField("Ordonnance", validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField("Mettre à jour")

class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_genre_delete_wtf = StringField("Effacer cet apprenti")
    submit_btn_del = SubmitField("Effacer apprenti")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
