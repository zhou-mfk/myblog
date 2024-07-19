from flask_bootstrap import Bootstrap  # type: ignore[import-untyped]
from flask_ckeditor import CKEditor  # type: ignore[import-untyped]
from flask_migrate import Migrate
from flask_moment import Moment  # type: ignore[import-untyped]
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

bootstrap = Bootstrap()
migrate = Migrate()
ckeditor = CKEditor()
moment = Moment()
