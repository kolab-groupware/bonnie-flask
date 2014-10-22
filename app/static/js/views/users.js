// global define
define([
    'jquery',
    'underscore',
    'backbone',
    'handlebars',
    'text!templates/users.html',
    'text!templates/userlistitem.html'
], function ($, _, Backbone, Handlebars, tmplUsers, tmplListItem) {
    "use strict";

    var UserListItemView = Backbone.View.extend({

        tagName: 'tr',
        className: 'user',

        template: Handlebars.compile(tmplListItem),

        events: {
            'click .btn-edituser': 'editUser'
        },

        initialize: function() {
            
        },

        render: function() {
            this.$el.html(this.template(this.model.attributes));
            return this;
        },

        editUser: function(e) {
            App.router.navigate('users/' + this.model.id, { trigger: true });
            return false;
        }

    });

    var UsersView = Backbone.View.extend({

        route: 'users',

        className: 'container backbone-view',

        template: Handlebars.compile(tmplUsers),

        // Delegated events from UI elements within this view
        events: {
            'click #btn-adduser':  'addUser',
        },

        initialize: function() {
            this.collection.on('reset', this.render, this);
            this.collection.on('add', this.render, this);
        },

        render: function() {
            if (!this._initialized) {
                // render main view template
                this.$el.html(this.template())
                    .appendTo('body')
                    .show();

                this._initialized = true;
            }
            else {
                this.$el.find('.records').html('')
            }

            var table = this.$el.find('.records');

            _.each(this.collection.models, function(user) {
                var itemview = new UserListItemView({ model: user })
                table.append(itemview.render().el);
            }, this);

            return this;
        },

        addUser: function() {
            App.router.navigate('users/_new_', { trigger: true });
        }

    });

    return UsersView;
});