from flask_ckeditor import CKEditorField  # type: ignore
from flask_wtf import FlaskForm  # type: ignore
from sqlalchemy import select
from wtforms import (  # type: ignore
    BooleanField,
    HiddenField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import (  # type: ignore
    URL,
    DataRequired,
    Email,
    Length,
    Optional,
)

from myblog.ext import db
from myblog.models import Category


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(1, 60)])
    category = SelectField("Category", coerce=int, default=1)
    body = CKEditorField("Body", validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (category.id, category.name)
            for category in db.session.execute(
                select(Category).order_by(Category.name).all()
            )
        ]


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if db.session.execute(
            select(Category).where(Category.name == field.data).first()
        ):
            raise ValidationError("Name already in use.")


class CommentForm(FlaskForm):
    author = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField("Site", validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()
