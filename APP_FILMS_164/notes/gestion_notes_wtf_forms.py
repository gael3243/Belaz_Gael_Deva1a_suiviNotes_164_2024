from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired

class FormWTFAjouterNotes(FlaskForm):
    notes_wtf = StringField("Note", validators=[DataRequired(), Length(min=1, max=50), Regexp(r"", message="Caractères alphabétiques uniquement")])
    fk_matiere_wtf = StringField("Matière", validators=[DataRequired(), Length(min=1, max=50)])
    fk_typeNotes_wtf = StringField("Type de notes", validators=[DataRequired(), Length(min=1, max=50)])
    fk_apprenti_wtf = StringField("Apprenti", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("Ajouter")

class FormWTFUpdateNotes(FlaskForm):
    notes_update_wtf = StringField("Notes", validators=[DataRequired(), Length(min=1, max=50)])
    fk_matiere_update_wtf = StringField("Matière", validators=[DataRequired(), Length(min=1, max=50)])
    fk_typeNotes_update_wtf = StringField("Type de notes", validators=[DataRequired(), Length(min=1, max=50)])
    fk_apprenti_update_wtf = StringField("Apprenti", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("Mettre à jour")

class FormWTFDeleteNotes(FlaskForm):
    """
        Dans le formulaire "notes_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    notes_delete_wtf = StringField("Effacer cette notes")
    submit_btn_del = SubmitField("Effacer apprenti")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
