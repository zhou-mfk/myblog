from flask_bootstrap import Bootstrap4  # type: ignore
from flask_ckeditor import CKEditor  # type: ignore
from flask_login import LoginManager  # type: ignore
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect  # type: ignore
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


db = SQLAlchemy(model_class=Base)

bootstrap = Bootstrap4()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
ckeditor = CKEditor()
