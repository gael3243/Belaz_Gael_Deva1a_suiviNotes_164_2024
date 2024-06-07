from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired

class FormWTFAjouterTypeMatiere(FlaskForm):
    type_matiere_wtf = StringField("Nom matière", validators=[DataRequired(), Length(min=1, max=50), Regexp(r"", message="Caractères alphabétiques uniquement")])
    submit = SubmitField("Ajouter")

class FormWTFUpdateTypeMatiere(FlaskForm):
    type_matiere_update_wtf = StringField("matière", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("Mettre à jour")

class FormWTFDeleteTypeMatiere(FlaskForm):
    """
        Dans le formulaire "matipre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    type_matiere_delete_wtf = StringField("Effacer cette matière")
    submit_btn_del = SubmitField("Effacer apprenti")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
