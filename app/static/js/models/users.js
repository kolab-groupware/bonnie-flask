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
                return "Username is required";
            }
            if (attributes['password'] && attributes['password'].length < 5) {
                return "Password too short";
            }
            if (attributes['password'] && attributes['password'] != attributes['password-check']) {
                return "Password repeat doesn't match";
            }
            if ((attributes['permissions'] & 1) && !attributes['secret']) {
                return "Please set a secret key for API access";
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
