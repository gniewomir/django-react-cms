const {AuthenticationError} = require('apollo-server');
const {to} = require('await-to-js');

const throwAuthenticationError = (error) => {
    if (error instanceof AuthenticationError) {
        throw error
    }
    throw new AuthenticationError(error);
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
        exchangeToken: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.getCurrentUser());
            if (error) {
                throwAuthenticationError(error);
            }
            console.log(user);
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
        acceptPrivacyPolicy: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.update({'accepted_privacy_policy': true}));
            if (error) {
                throwAuthenticationError(error);
            }
            user.token = user.elevated_token ? user.elevated_token : user.identity_token;
            user.is_loggedin = !!user.elevated_token;
            return user;
        },
        collectEmail: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.update(args.input));
            if (error) {
                throwAuthenticationError(error);
            }
            user.token = user.elevated_token ? user.elevated_token : user.identity_token;
            user.is_loggedin = !!user.elevated_token;
            return user;
        },
        registerUser: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.update(args.input));
            if (error) {
                throwAuthenticationError(error);
            }
            user.token = user.elevated_token ? user.elevated_token : user.identity_token;
            user.is_loggedin = !!user.elevated_token;
            return user;
        },
        loginUser: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.login(args.input));
            if (error) {
                throwAuthenticationError(error);
            }
            user.token = user.elevated_token ? user.elevated_token : user.identity_token;
            user.is_loggedin = !!user.elevated_token;
            return user;
        },
        updateUser: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.update(args.input));
            if (error) {
                throwAuthenticationError(error);
            }
            user.token = user.elevated_token ? user.elevated_token : user.identity_token;
            user.is_loggedin = !!user.elevated_token;
            return user;
        },
        logoutUser: async (parent, args, {dataSources}) => {
            const [error, user] = await to(dataSources.AccountsService.logout());
            if (error) {
                throwAuthenticationError(error);
            }
            user.token = user.elevated_token ? user.elevated_token : user.identity_token;
            user.is_loggedin = !!user.elevated_token;
            return user;
        },
    }
};

module.exports = resolvers;