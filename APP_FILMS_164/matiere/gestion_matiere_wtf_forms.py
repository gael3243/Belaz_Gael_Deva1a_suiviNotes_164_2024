from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired

class FormWTFAjouterMatiere(FlaskForm):
    nom_matiere_wtf = StringField("Nom matière", validators=[DataRequired(), Length(min=1, max=50), Regexp(r"", message="Caractères alphabétiques uniquement")])
    fk_type_matiere_wtf = StringField("FK matière", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("Ajouter")

class FormWTFUpdateMatiere(FlaskForm):
    nom_matiere_update_wtf = StringField("matière", validators=[DataRequired(), Length(min=1, max=50)])
    fk_type_matiere_update_wtf = StringField("Matière", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("Mettre à jour")

class FormWTFDeleteMatiere(FlaskForm):
    """
        Dans le formulaire "matipre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_matiere_delete_wtf = StringField("Effacer cette matière")
    submit_btn_del = SubmitField("Effacer apprenti")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
