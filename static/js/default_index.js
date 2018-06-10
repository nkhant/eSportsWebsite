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
            });
    };

    self.add_article = function () {
        // The submit button to add an article has been added.
        $.post(add_article_url,
            {
                title : self.vue.title_holder,
                author : self.vue.author_holder,
                content: self.vue.content_holder,
                game : self.vue.game_holder,

            },
            function (data) {
                // $.web2py.enableElement($("#add_memo_submit"));
                self.vue.articles.unshift(data.article);
                enumerate(self.vue.articles);
                self.get_articles();
            });

    };

    self.redirect_to_article = function(article_displayed){
        self.vue.page = 'display_article';
        self.vue.article_displayed = article_displayed;
    }


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            logged_in: null,
            articles : [],
            title_holder: null,
            author_holder: null,
            content_holder: null,
            created_on_holder: null,
            game_holder: null,
            is_creator: false,
            page: 'main_page',
            article_displayed: null

        },
        methods: {
            add_article : self.add_article,
            get_articles : self.get_articles,
            redirect_to_article: self.redirect_to_article,
        }

    });

    self.get_articles();
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
