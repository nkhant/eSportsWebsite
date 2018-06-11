from operator import itemgetter
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
    rows = db().select(db.Articles.ALL, orderby=~db.Articles.Created_On)
    for i, r in enumerate(rows):
            # Find the sum of all the like counter for this particular article
            # Basically, get the total number of likes for every article
            counter = 0
            if db(db.Fav_Articles.id > 0).isempty() == False:
                for row in db((db.Fav_Articles.id > 0) & (r.id == db.Fav_Articles.Article_id)).select():
                    counter = counter + row.like_counter
            t = dict(
                id = r.id,
                title = r.Title,
                author=r.Author,
                description = r.Article_Description,
                content = r.Article_Content,
                created_on = r.Created_On,
                game = r.Game,
                index = r.id,
                like_counter = counter
            )
            articles.append(t)
    
    articles = sorted(articles, key=itemgetter('like_counter'), reverse=True)

    logged_in = auth.user is not None
    return response.json(dict(
        articles=articles,
        logged_in=logged_in,
        user_type=user_type
    ))

def get_submitted_articles():
    articles = []
    # Check if user is logged in
    # This handles the case when the user logs out and get_submitted_articles is called
    if auth.user != None:
        # Iterate through articles db and append articles that are created by the currently logged in user
        for row in db((db.Articles > 0) & (db.Articles.created_by == auth.user)).select(orderby=~db.Articles.Created_On):
            # Find the sum of all the like counter for this particular article
            # Basically, get the total number of likes for every article
            counter = 0
            if db(db.Fav_Articles.id > 0).isempty() == False:
                for r in db((db.Fav_Articles.id > 0) & (row.id == db.Fav_Articles.Article_id)).select():
                    counter = counter + r.like_counter
            t = dict(
                title = row.Title,
                author=row.Author,
                content = row.Article_Content,
                created_on = row.Created_On,
                game = row.Game,
                index = row.id,
                like_counter = counter
            )
            articles.append(t)
    return response.json(dict(
        articles=articles
    ))

def get_fav_articles():
    articles = []
    # Check if user is logged in
    # This handles the case when the user logs out and get_fav_articles is called
    if auth.user != None:
        # Iterate through Fav_Articles
        for row in db((db.Fav_Articles.id > 0) & (db.Fav_Articles.favorited_by == auth.user.id)).select():
            # For every Fav_Article id iterate through Articles
            for r in db((db.Articles.id > 0) & (row.Article_id == db.Articles.id) & (row.favorited_by == auth.user.id)).select():
                # Get the total number of likes for the article favorited by the logged in user
                counter = 0
                if db(db.Fav_Articles.id > 0).isempty() == False:
                    for rsum in db((db.Fav_Articles.id > 0) & (r.id == db.Fav_Articles.Article_id)).select():
                        counter = counter + rsum.like_counter
                # For every Article that is a Fav_article of the currently logged in user, get its attributes and
                # store them as an object and store that object into an array
                t = dict(
                    title = r.Title,
                    author=r.Author,
                    content = r.Article_Content,
                    created_on = r.Created_On,
                    game = r.Game,
                    index = r.id,
                    like_counter = counter
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
        Created_By=auth.user,
        Game=request.vars.game
    )

    t = db.Articles(t_id)
    return response.json(dict(
        article=t
    ))

@auth.requires_signature()
def add_fav_article():
    # Iterate through all favorited articles and only like an article if it has not been liked by logged in user already
    # Otherwise unlike

    # This checks if user already liked the article
    # If the article liked by user exists in Fav_Articles then it means the user already liked the article
    # In this case unlike the article
    trigger = False
    skipIF = False
    for row in db((db.Fav_Articles.id > 0) & (db.Fav_Articles.Article_id == request.vars.index) & (auth.user.id == db.Fav_Articles.favorited_by)).select():
        if row.like_toggle == True:
            subtraction = row.like_counter - 1
            row.update_record( like_counter = subtraction )
            row.update_record( like_toggle = False )
            row.update_record( favorited_by = None )
            # This prevents a like to be added to the article
            trigger = True
            # Prevents below for loop from running
            skipIF = True

    if skipIF != True:
        # Checks in the case fav article is alreadly inserted and toggled at least once
        for row in db((db.Fav_Articles.id > 0) & (db.Fav_Articles.Article_id == request.vars.index) & (auth.user.id == db.Fav_Articles.favorited_by)).select():
            if row.like_toggle == False:
                addition = row.like_counter + 1
                row.update_record( like_counter = addition )
                row.update_record( like_toggle = True )
                row.update_record( favorited_by = auth.user.id )
                # This prevents a like to be added to the article
                trigger = True

    # Add a like if the logged in user has not liked this article before
    if trigger != True: 
        # Insert the article index and the current user id
        t_id = db.Fav_Articles.insert(
            Article_id=request.vars.index,
            favorited_by=auth.user.id,
            like_counter=1,
            like_toggle=True
        )
        # For possible debugging purposes
        t = db.Fav_Articles(t_id)

    return response.json(dict(
        user=auth.user
    ))
