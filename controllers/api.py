# Here go your api methods.

def get_articles():
    user_type = None
    # Check if user is logged in
    if auth.user != None:
        # Search the auth_user db for the currently logged in user
        # Get the currently logged in user's user type
        for row in db((db.auth_user.id > 0) & (db.auth_user.id == auth.user.id)).select():
            user_type = row.user_type

    # start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    # end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    articles = []
    # has_more = False
    rows = db().select(db.Articles.ALL)
    for i, r in enumerate(rows):
            t = dict(
                id = r.id,
                title = r.Title,
                author=r.Author,
                description = r.Article_Description,
                content = r.Article_Content,
                created_on = r.Created_On,
                game = r.Game,
                index = r.id
            )
            articles.append(t)
    logged_in = auth.user is not None
    return response.json(dict(
        articles=articles,
        logged_in=logged_in,
        user_type=user_type
    ))

def get_fav_articles():
    articles = []
    # Check if user is logged in
    # This handles the case when the user logs out and get_fav_articles is called
    if auth.user != None:
        # Iterate through Fav_Articles
        for row in db(db.Fav_Articles.id > 0).select():
            # For every Fav_Article id iterate through Articles
            for r in db((db.Articles.id > 0) & (row.Article_id == db.Articles.id) & (row.favorited_by == auth.user.id)).select():
                # For every Article that is a Fav_article of the currently logged in user, get its attributes and
                # store them as an object and store that object into an array
                t = dict(
                    title = r.Title,
                    author=r.Author,
                    content = r.Article_Content,
                    created_on = r.Created_On,
                    game = r.Game,
                    index = r.id
                )
                # Then append the element to articles array
                articles.append(t)
    return response.json(dict(
        articles=articles
    ))

@auth.requires_signature()
def add_article():

    t_id = db.Articles.insert(
        Title=request.vars.title,
        Author=request.vars.author,
        Article_Description=request.vars.description,
        Article_Content=request.vars.content,
        Game=request.vars.game
    )

    t = db.Articles(t_id)
    return response.json(dict(
        article=t
    ))

@auth.requires_signature()
def add_fav_article():
    # Insert the article index and the current user id
    t_id = db.Fav_Articles.insert(
        Article_id=request.vars.index,
        favorited_by=auth.user.id
    )

    t = db.Articles(t_id)
    return response.json(dict(
        article=t
    ))
