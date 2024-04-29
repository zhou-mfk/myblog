from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from myblog import create_app, db

app = create_app("dev")


# manager 来进行 app 实例操作，如服务启动、端口重置等
manager = Manager(app)

# 把Flask程序实例app和SQLAlchemy实例db作为参数传递给 flask_migrate 提供的 Migrate类，初始化Migrate实例 migrate
migrate = Migrate(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
