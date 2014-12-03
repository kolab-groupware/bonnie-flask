// global define
define([
    'backbone'
], function (Backbone) {
    "use strict";

    var Permission = {
        API_ACCESS: 1,
        WEB_ACCESS: 2,
        ADMINISTRATOR: 128
    };

    var User = Backbone.Model.extend({

        urlRoot: "/data/users",

        idAttribute: "id",

        Permission: Permission,

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
            if ((attributes['permissions'] & Permission.API_ACCESS) && !attributes['secret']) {
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
        UserCollection: UserCollection,
        Permission: Permission
    };
});
