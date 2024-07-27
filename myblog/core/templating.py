from flask_login import current_user  # type: ignore
from sqlalchemy import func, select

from myblog.core.ext import db
from myblog.models import Admin, Category, Comment


def register_template_handlers(app):
    @app.context_processor
    def make_template_context():
        admin = db.session.execute(select(Admin)).scalar()
        categories = (
            db.session.execute(select(Category).order_by(Category.name)).scalars().all()
        )
        # link

        if current_user.is_authenticated:
            unread_comments = (
                db.session.execute(
                    select(func.count(Comment.id)).filter_by(reviewed=False)
                )
                .scalars()
                .one()
            )
        else:
            unread_comments = None

        return dict(admin=admin, categories=categories, unread_comments=unread_comments)
