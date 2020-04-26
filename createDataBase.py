from myblog import app
from myblog import db


def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
