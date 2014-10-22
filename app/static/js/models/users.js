// global define
define([
    'backbone'
], function (Backbone) {
    "use strict";

    var User = Backbone.Model.extend({

        urlRoot: "/data/users",

        idAttribute: "id",

        initialize: function() {

        },

        parse: function(attrib, options) {
            // TODO: translate attrib.permissions
            return attrib;
        },

        validate: function(attributes, options) {
            if (!attributes['username'] || attributes['username'].replace(/(^\s+)|(\s+)$/, '') == '') {
                return App._("Username is required");
            }
            if (attributes['password'] && attributes['password'].length < 5) {
                return App._("Password too short");
            }
            if (attributes['password'] && attributes['password'] != attributes['password-check']) {
                return App._("Password repeat doesn't match");
            }
            if ((attributes['permissions'] & 1) && !attributes['secret']) {
                return App._("Please set a secret key for API access");
            }
        }

    });

    var UserCollection = Backbone.Collection.extend({

        model: User,

        url: "/data/users"

    });

    return {
        User: User,
        UserCollection: UserCollection
    };
});
