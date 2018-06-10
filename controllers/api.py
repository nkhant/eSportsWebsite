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
                content = r.Article_Content,
                created_on = r.Created_On,
                game = r.Game,
            )
            articles.append(t)
    logged_in = auth.user is not None
    return response.json(dict(
        articles=articles,
        logged_in=logged_in,
        user_type=user_type
    ))


@auth.requires_signature()
def add_article():

    t_id = db.Articles.insert(
        Title=request.vars.title,
        Author=request.vars.author,
        Article_Content=request.vars.content,
        Game=request.vars.game,
    )

    t = db.Articles(t_id)
    print t
    return response.json(dict(
        article=t
    ))






