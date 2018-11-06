import fetch from 'node-fetch';
import gql from 'graphql-tag';
import {ApolloClient} from 'apollo-client';
import {createHttpLink} from 'apollo-link-http';
import {InMemoryCache} from 'apollo-cache-inmemory';


export const createAuthorizationMiddleware = () => {

    return async (req, res, next) => {
        try {
            const headers = req.header('authorization') || req.cookies.authorization ? {
                authorization: req.header('authorization') || req.cookies.authorization
            } : {};
            if (headers.authorization && headers.authorization.substring(0, 5) !== 'Token') {
                res.status(401).send('Wrong authentication method!')
            }
            const client = new ApolloClient({
                ssrMode: true,
                link: createHttpLink({
                    uri: process.env.SERVICE_URL_GRAPHQL,
                    credentials: 'same-origin',
                    headers,
                    fetch
                }),
                cache: new InMemoryCache(),
            });
            const user = await client.query({
                query: gql`
                    query {
                      userIdentity {
                        token
                      }
                    }
                `,
            });
            // update cookie every time in case user logged in or logged out
            res.cookie('authorization', `Token ${user.data.userIdentity.token}`, {
                httpOnly: true,
                secure: true,
                maxAge: 60 * 60 * 24 * 365 * 20 * 1000
            });
            res.locals.client = client;
            res.locals.user = user;
            next();
        } catch (error) {
            res.status(401).send('Authentication error!')
        }
    }
};


