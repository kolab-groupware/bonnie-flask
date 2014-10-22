// global define
define([
    'jquery',
    'backbone',
    'handlebars',
    'text!templates/userform.html'
], function ($, Backbone, Handlebars, tplForm) {
    "use strict";

    return Backbone.View.extend({

        route: 'users',

        className: 'container backbone-view',

        template: Handlebars.compile(tplForm),

        // Delegated events from UI elements within this view
        events: {
            'click .btn-save':   'saveUser',
            'click .btn-delete': 'deleteUser',
            'click .btn-generate-secret': 'generateSecret',
            'keyup input':       'changed',
            'change input':      'changed',
            'change select':     'changed'
        },

        initialize: function() {

        },

        render: function() {
            this.$el.html(this.template(this.model.attributes))
                .appendTo('body')
                .show();

            if (this.model.isNew()) {
                this.$el.find('h1').text('Create New User');
                this.$el.find('.btn-delete').hide();
            }
            if (this.model.get('_isme')) {
                this.$el.find('.btn-delete').hide();
                this.$el.find('#ff-user-permissions').closest('.form-group').hide();
            }

            this.$el.find('.btn-save').prop('disabled', true);

            // set permission options
            var rights = this.model.get('permissions')
            this.$el.find('#ff-user-permissions option').each(function(i,opt) {
                var val = parseInt(opt.value);
                opt.selected = (val & rights) > 0;
            });

            // reset changed state...
            this.model.set(this.model.attributes);

            return this;
        },

        /**
         * Triggered when a form field was changed
         */
        changed: function(evt) {
            var target = $(evt.currentTarget),
                value = target.val(), data = {};

            // convert selected permission options into a bitset
            if (evt.currentTarget.nodeName == 'SELECT') {
                value = 0;
                target.children().each(function(i,opt) {
                    if (opt.selected) {
                        value |= parseInt(opt.value);
                    }
                });
            }

            if (value != this.model.get(target.attr('name'))) {
                data[target.attr('name')] = value;
                this.model.set(data);
                this.$el.find('.btn-save').prop('disabled', !this.model.hasChanged());
            }
        },

        saveUser: function(e) {
            var me = this, isnew = this.model.isNew();
            if (this.model.hasChanged()) {
                // validate data before submitting
                if (!this.model.isValid()) {
                    UI.flash("User data is not valid: " + this.model.validationError, 'warning');
                    this.model.set(this.model.attributes);
                    return false;
                }

                me.$el.find('.btn-save').prop('disabled', false);

                this.model.save({}, {
                    success: function(model, response) {
                        // show confirmation message
                        UI.flash('Saved successfully', 'success');

                        if (response.id) {
                            App.router.navigate('users/' + response.id, { trigger: true });
                        }
                    },
                    error: function(model, response) {
                        UI.flash('Error saving user! ' + (response.responseJSON.error || ''), 'danger');
                        me.$el.find('.btn-save').prop('disabled', false);
                    }
                });
            }
            return false;
        },

        deleteUser: function() {
            var me = this;
            UI.confirm('Do you really want to delete user ' + this.model.username + '?', 'Delete User', function() {
                me.model.destroy({
                    success: function(model, response) {
                        UI.flash('Successfully deleted user', 'success');
                        App.router.navigate('users', { trigger: true });
                    },
                    error: function(model, response) {
                        UI.flash('Error deleting user:' + (response || ''), 'danger');
                    }
                });
            });
        },

        generateSecret: function() {
            var chars = "0123456789-abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRTSUVWXYZ/*+=$:;",
                i, len = 64, secret = '';

            while (secret.length < len) {
                i = Math.floor(Math.random() * (chars.length - 1));
                secret += chars.charAt(i);
            }

            this.$el.find('#ff-user-secret').val(secret).change();
        }

    });
});