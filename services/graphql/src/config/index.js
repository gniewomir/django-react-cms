module.exports = {
    secret: process.env.SECRET_KEY,
    services: {
        accounts: process.env.SERVICE_URL_ACCOUNTS,
        cms:      process.env.SERVICE_URL_CMS,
        redis:    process.env.SERVICE_URL_REDIS,
        graphql:  process.env.SERVICE_URL_GRAPHQL
    }
};
