"use strict";

///// globals

var App = {
    _: function(s) { return s }
};
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
            '<button type="button" class="btn btn-default" data-dismiss="modal">' + App._('Cancel') + '</button>' +
            '<button type="button" class="btn btn-primary" data-dismiss="modal">' + App._('Confirm') + '</button>' +
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
        },
        'i18next': {
            exports: 'i18n'
        }
    },

    paths: {
        text: "libs/require-text",
        backbone: "libs/backbone-min",
        underscore: "libs/underscore-min",
        handlebars: "libs/handlebars-v2.0.0",
        i18next: "libs/i18next.amd-1.7.4.min",
        templates: "templates"
    }
});

require(['backbone', 'i18next', 'handlebars', 'routers/main', 'views/nav'], function (Backbone, i18n, Handlebars, Router, NavView) {
    // initialize i18n
    var opts = {
        ns: 'bonnie-client',
        lng: 'en',
        fallbackLng: 'en',
        preload: ['en'],
        interpolationPrefix: '%(',
        interpolationSuffix: ')s',
        resGetPath: '/static/js/locales/%(lng)s/%(ns)s.json',
        // enable during development:
        sendMissing: true,
        missingKeyHandler: function(lng, ns, key, defaultValue, lngs) {
            console.log("Missing locale:", ns, lng, '"' + key + '"');
        }
    };
    i18n.init(opts, function(t) {
        App._ = t;
        Handlebars.registerHelper('_', function(key) {
            return new Handlebars.SafeString(t(key));
        });
    });

    // initialize routing and start Backbone.history()
    App.router = new Router();
    Backbone.history.start();

    // connect router with main navigation
    App.nav = new NavView({ router:App.router });
});
