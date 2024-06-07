from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired

class FormWTFAjouterTypeNotes(FlaskForm):
    type_notes_wtf = StringField("Matière", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("Ajouter")

class FormWTFUpdateTypeNotes(FlaskForm):
    type_notes_update_wtf = StringField("Matière", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("Mettre à jour")

class FormWTFDeleteTypeNotes(FlaskForm):
    """
        Dans le formulaire "notes_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    type_notes_delete_wtf = StringField("Effacer cet apprenti")
    submit_btn_del = SubmitField("Effacer apprenti")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
