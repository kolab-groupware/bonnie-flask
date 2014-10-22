"use strict";

///// globals

var App = {};
var UI = {};

/**
 * Display a flash message
 */
UI.flash = function(message, type, timeout) {
    var div = $('<div>')
        .attr('role', 'alert')
        .addClass('fade in alert alert-' + (type || 'info'))
        .append('<button type="button" class="close" data-dismiss="alert">&times;</button>')
        .append(message)
        .appendTo('#flash-container')
        .alert();

    if (type != 'danger' && timeout !== 0) {
        setTimeout(function(){ div.alert('close') }, (timeout || 5) * 1000)
    }

    // TODO: scroll message into sight

    return div;
};

/**
 * Show a Bootstrap modal confirmation dialog
 */
UI.confirm = function(message, title, ack, nack) {
    var html = '<div class="modal fade">' +
      '<div class="modal-dialog">' +
        '<div class="modal-content">' +
          '<div class="modal-header">' +
            '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>' +
            '<h4 class="modal-title"></h4>' +
          '</div>' +
          '<div class="modal-body">' +
            '<p></p>' +
          '</div>' +
          '<div class="modal-footer">' +
            '<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>' +
            '<button type="button" class="btn btn-primary" data-dismiss="modal">Confirm</button>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>';

    var dialog = $(html)
        .appendTo('body')
        .on('click', '.btn-primary', function(e) {
            nack = undefined;
            if (typeof ack == 'function')
                ack();
        })
        .on('click', '.btn-default', function(e) {
            if (typeof nack == 'function')
                nack();
        })
        .on('shown.bs.modal', function(e) {
            $(this).find('.btn-primary').focus();
        })
        .on('hide.bs.modal', function(e) {
            if (typeof nack == 'function')
                nack();
            $(this).remove();
        });

    dialog.find('.modal-title').text(title);
    dialog.find('.modal-body p').text(message);
    dialog.modal({ keyboard: false });
};


// use jQuery object already available from Bootstrap
define("jquery", [], function() { return jQuery; });

require.config({
    // baseUrl: 'js/lib',

    shim: {
        'underscore': {
            exports: "_"
        },

        'backbone': {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },

        'handlebars': {
            exports: 'Handlebars'
        }
    },

    paths: {
        text: "libs/require-text",
        backbone: "libs/backbone-min",
        underscore: "libs/underscore-min",
        handlebars: "libs/handlebars-v2.0.0",
        templates: "templates"
    }
});

require(['backbone', 'routers/main', 'views/nav'], function (Backbone, Router, NavView) {
    // initialize routing and start Backbone.history()
    App.router = new Router();
    Backbone.history.start();

    // connect router with main navigation
    App.nav = new NavView({ router:App.router });
});
