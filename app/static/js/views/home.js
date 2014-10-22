// global define
define([
    'jquery',
    'backbone'
], function ($, Backbone) {
    "use strict";

    // Our overall **MainView** is the top-level piece of UI.
    return Backbone.View.extend({

        route: '',

        el: '#view-home',

        // Delegated events from UI elements within this view
        events: {
            //'click #clear-completed':    'clearCompleted',
            //'click #toggle-all':        'toggleAllComplete'
        },

        initialize: function() {

        },

        render: function() {
            this.$el.show();
            return this;
        },

        remove: function() {
            this.stopListening();
            this.$el.hide();
            return this;
        }

    });
});