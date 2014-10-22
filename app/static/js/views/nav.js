// global define
define([
    'jquery',
    'backbone'
], function ($, Backbone) {
    "use strict";

    return Backbone.View.extend({
        el: '#mainnav',

        initialize: function(args) {
            this.router = args.router || Backbone.Events;
            this.router.on('setroute', this.render, this);
        },

        render: function() {
            this.$el.find('li.active').removeClass('active')
            if (this.router.activeView && this.router.activeView.route) {
                this.$el.find('li.route-' + this.router.activeView.route).addClass('active')
            }
        }
    });
});