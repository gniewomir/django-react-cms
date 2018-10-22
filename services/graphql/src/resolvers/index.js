const resolvers = {
    Query: {
        userIdentity: async (parent, args, {dataSources}) => {
            return dataSources.AccountsService.getCurrentUser();
        },
        user: (parent, args, {dataSources}) => {
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