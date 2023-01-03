from main import db,app, User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))