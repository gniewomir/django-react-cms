const {AuthenticationError} = require('apollo-server');
const {to} = require('await-to-js');

const throwAuthenticationError = (error) => {
    if (error instanceof AuthenticationError) {
        throw error
    }
    throw AuthenticationError(error);
};

const resolvers = {
    Query: {
        userIdentity: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.getCurrentUser());
            if (error) {
                throwAuthenticationError(error);
            }
            user.token = user.elevated_token ? user.elevated_token : user.identity_token;
            user.is_loggedin = !!user.elevated_token;
            return user;
        },
        userInfo: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.getCurrentUser());
            if (error) {
                throwAuthenticationError(error);
            }
            user.token = user.elevated_token ? user.elevated_token : user.identity_token;
            user.is_loggedin = !!user.elevated_token;
            return user;
        },
        user: (parent, args, {dataSources, auth_method}) => {
            if (auth_method !== 'jwt') {
                throwAuthenticationError('Invalid authorization method!');
            }
            return dataSources.AccountsService.getCurrentUser();

        }
    },
    Mutation: {
        acceptPrivacyPolicy: (parent, args, {dataSources}) => {
            return dataSources.AccountsService.update({'accepted_privacy_policy': true});
        },
        collectEmail: (parent, args, {dataSources}) => {
            return dataSources.AccountsService.update(args.input);
        },
        registerUser: (parent, args, {dataSources}) => {
            return dataSources.AccountsService.update(args.input);
        },
        loginUser: (parent, args, {dataSources}) => {
            return dataSources.AccountsService.login(args.input);
        },
        updateUser: (parent, args, {dataSources}) => {
            return dataSources.AccountsService.update(args.input);
        },
        logoutUser: (parent, args, {dataSources}) => {
            return dataSources.AccountsService.logout();
        },
    }
};

module.exports = resolvers;