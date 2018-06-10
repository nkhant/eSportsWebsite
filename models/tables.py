# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

def get_user_email():
    return auth.user.email if auth.user is not None else None


# Table for displaying articles
db.define_table('Articles',
                  Field('Title', 'text', default='null'),
                  Field('Author', 'text', default='null'),
                  Field('Article_Content', 'text', default='null'),
                  Field('Created_On', 'datetime', default=request.now),
                  Field('Game', 'text'),
                  Field('created_by', 'reference auth_user', default=auth.user_id)
               )

db.define_table('Fav_Articles',
                  Field('Article_id', 'integer', default=None),
                  Field('favorited_by', 'integer', default=None)
               )

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
