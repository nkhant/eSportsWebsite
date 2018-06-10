// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Enumerates an array.
    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};


    // Gets article and login info
    self.get_articles = function () {
        $.getJSON(get_articles_url,
            function (data) {
                self.vue.articles = data.articles;
                self.vue.logged_in = data.logged_in;
                enumerate(self.vue.articles);

                if (data.user_type == 'Reader') {
                    self.vue.is_creator = false;
                } else if (data.user_type == 'Creator') {
                    self.vue.is_creator = true;
                } else if (data.user_type == null) {
                    self.vue.is_creator = false;
                }
<<<<<<< HEAD
            });
    };

    self.get_fav_articles = function () {
        $.getJSON(get_fav_articles_url,
            function (data) {
                self.vue.fav_articles = data.articles;  
            });
    }
=======
            });
    };
>>>>>>> 7196d4da26eb6ce3f8b3bf97b9b9634b5e85d8e4

    self.add_article = function () {
        // The submit button to add an article has been added.
        $.post(add_article_url,
            {
                title: self.vue.title_holder,
                author: self.vue.author_holder,
                content: self.vue.content_holder,
                game: self.vue.game_holder

            },
            function (data) {
                console.log(data.article);
                // $.web2py.enableElement($("#add_memo_submit"));
                self.vue.articles.unshift(data.article);
                enumerate(self.vue.articles);
                self.get_articles();
            });

    };

<<<<<<< HEAD
    self.add_fav_article = function (index) {
        $.post(add_fav_article_url,
            {
                index: index
            },
            function (data) {
                self.get_fav_articles();
            });
    }

    self.test = function (content){
        console.log(content)
    };
=======
    self.redirect_to_article = function(article_displayed){
        self.vue.page = 'display_article';
        self.vue.article_displayed = article_displayed;
    }

>>>>>>> 7196d4da26eb6ce3f8b3bf97b9b9634b5e85d8e4

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            logged_in: null,
            articles : [],
            fav_articles: [],
            title_holder: null,
            author_holder: null,
            content_holder: null,
            created_on_holder: null,
            game_holder: null,
<<<<<<< HEAD
            is_creator: false
=======
            is_creator: false,
            page: 'main_page',
            article_displayed: null
>>>>>>> 7196d4da26eb6ce3f8b3bf97b9b9634b5e85d8e4

        },
        methods: {
            add_article : self.add_article,
            get_articles : self.get_articles,
<<<<<<< HEAD
            add_fav_article : self.add_fav_article,
            get_fav_articles : self.get_fav_articles,
            test : self.test
=======
            redirect_to_article: self.redirect_to_article,
>>>>>>> 7196d4da26eb6ce3f8b3bf97b9b9634b5e85d8e4
        }

    });

    self.get_fav_articles();
    self.get_articles();
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
