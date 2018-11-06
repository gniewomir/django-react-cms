const {AuthenticationError} = require('apollo-server');
const {to} = require('await-to-js');

const throwAuthenticationError = (error) => {
    if (error instanceof AuthenticationError) {
        throw error
    }
    throw new AuthenticationError(error);
};

const getCurrentUser = async (parent, args, {dataSources, user, token}) => {
    const [error, freshUser] = await to(dataSources.AccountsService.getCurrentUser());
    if (error) {
        throwAuthenticationError(error);
    }
    freshUser.token = token;
    freshUser.is_loggedin = token && token === user.elevated_token;
    return freshUser;
};

const getUpdatedUser = (user, token) => {
    user.token = token;
    user.is_loggedin = token && token === user.elevated_token;
    return user;
}

const resolvers = {
    Query: {
        userIdentity: getCurrentUser,
        exchangeToken: getCurrentUser,
        userInfo: getCurrentUser,
        user: (parent, args, {dataSources, token, auth_method}) => {
            if (auth_method !== 'jwt') {
                throwAuthenticationError('Invalid authorization method!');
            }
            return getCurrentUser(parent, args, {dataSources, token});
        }
    },
    Mutation: {
        acceptPrivacyPolicy: async (parent, args, {dataSources, token}) => {
            const [error, user] = await to(dataSources.AccountsService.update({"accepted_privacy_policy": true}));
            if (error) {
                throwAuthenticationError(error);
            }
            return getUpdatedUser(user, token);
        },
        collectEmail: async (parent, args, {dataSources, token}) => {
            const [error, user] = await to(dataSources.AccountsService.update(args.input));
            if (error) {
                throwAuthenticationError(error);
            }
            return getUpdatedUser(user, token);
        },
        registerUser: async (parent, args, {dataSources, token}) => {
            const [error, user] = await to(dataSources.AccountsService.update(args.input));
            if (error) {
                throwAuthenticationError(error);
            }
            return getUpdatedUser(user, token);
        },
        loginUser: async (parent, args, {dataSources, token}) => {
            const [error, user] = await to(dataSources.AccountsService.login(args.input));
            if (error) {
                throwAuthenticationError(error);
            }
            return getUpdatedUser(user, token);
        },
        updateUser: async (parent, args, {dataSources, token}) => {
            const [error, user] = await to(dataSources.AccountsService.update(args.input));
            if (error) {
                throwAuthenticationError(error);
            }
            return getUpdatedUser(user, token);
        },
        logoutUser: async (parent, args, {dataSources, token}) => {
            const [error, user] = await to(dataSources.AccountsService.logout());
            if (error) {
                throwAuthenticationError(error);
            }
            return getUpdatedUser(user, token);
        },
    }
};

module.exports = resolvers;