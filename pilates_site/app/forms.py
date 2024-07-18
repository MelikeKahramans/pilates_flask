from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, URL 
from app.models import Category

class CategoryLinkForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    category_id = SelectField('Kategori', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Kaydet')

    def __init__(self, *args, **kwargs):
        super(CategoryLinkForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

class CategoryLinkForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    category_id = IntegerField('Kategori ID', validators=[DataRequired()])
    submit = SubmitField('Ekle')