from flask import Flask

from db_connect import db

from library.post_for_crate import post_bp
from library.services import services_bp
from library.views import views_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)

app.register_blueprint(post_bp)
app.register_blueprint(services_bp)
app.register_blueprint(views_bp)

if __name__ == '__main__':
    app.run(debug=True)
