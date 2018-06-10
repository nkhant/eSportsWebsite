# Here go your api methods.

def get_articles():
    # start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    # end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    articles = []
    # has_more = False
    rows = db().select(db.Articles.ALL)
    for i, r in enumerate(rows):
            t = dict(
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
    ))



def add_article():
    t_id = db.Articles.insert(
        Title=request.vars.title,
        Author=request.vars.author,
        Article_Content=request.vars.content,
        Game=request.vars.game,
    )
    t = db.Articles(t_id)
    return response.json(dict(article=t))


