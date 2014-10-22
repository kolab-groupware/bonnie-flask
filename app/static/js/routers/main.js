/*global define*/
define([
    'jquery',
    'backbone'
], function ($, Backbone) {
    "use strict";

    return Backbone.Router.extend({

        routes: {
            '': 'homeView',
            'users': 'usersView',
            'users/:id': 'userForm'
        },

        activeView: null,

        activateView: function(view) {
            if (this.activeView) {
                this.activeView.remove();
            }

            this.activeView = view;
            this.activeView.render();
            this.trigger('setroute', this);
        },

        homeView: function() {
            var me = this;
            require(['views/home'], function (HomeView) {
                me.activateView(new HomeView({ app:me }));
            });
        },

        usersView: function() {
            var me = this;
            require(['views/users', 'models/users'], function (UsersView, models) {
                var users = new models.UserCollection(),
                    view = new UsersView({ collection:users, model:new models.User() });
                me.activateView(view);
                users.fetch();
            });
        },

        userForm: function(id) {
            var me = this;
            require(['views/userform', 'models/users'], function (UserForm, models) {
                if (id == '_new_') {
                    var view = new UserForm({ model: new models.User() });
                    me.activateView(view);
                }
                else {
                    var user = new models.User({ id: id });
                    user.fetch({
                        success: function(data) {
                            var view = new UserForm({ model: data });
                            me.activateView(view);
                        },
                        error: function(model, response, options) {
                            UI.flash(App._('Failed to fetch user __id__', { id: id }), 'danger');
                        }
                    });
                }
            });
        }

    });
});