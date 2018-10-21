const {AuthenticationError} = require('apollo-server');
const {services: {accounts}, secret} = require('../config');
const fetch = require('node-fetch');
const {verify} = require('jsonwebtoken');
const {to} = require('await-to-js');

const create = async () => {
    const [response_error, response] = await to(fetch(`${accounts}/user/`, {method: 'post'}));
    if (response_error) {
        return Promise.reject(response_error);
    }
    const [decoding_error, json] = await to(response.json());
    if (decoding_error) {
        return Promise.reject(decoding_error);
    }
    if (!json.identity_token) {
        return Promise.reject('Cannot create user!');
    }
    return Promise.resolve({
        user: json,
        token: json.identity_token,
        loggedin: false
    });
};
const get = async (token) => {
    const [response_error, response] = await to(fetch(`${accounts}/user/${token}`));
    if (response_error) {
        return Promise.reject(response_error);
    }
    const [decoding_error, json] = await to(response.json());
    if (decoding_error) {
        return Promise.reject(decoding_error);
    }
    if (!json.identity_token) {
        return Promise.reject('Cannot create user!');
    }
    return Promise.resolve({
        user: json,
        token: token === json.elevated_token ? json.elevated_token : json.identity_token,
        loggedin: token === json.elevated_token
    });
};

const check = async (token) => {
    if (!secret) {
        return Promise.reject('Cannot validate JWT token!')
    }
    verify(token, secret, (err, user) => {
        if (err) {
            return Promise.reject(err);
        }
        return Promise.resolve({
            user,
            token,
            loggedin: !!user.elevated_token
        })
    });
};

module.exports = async ({req}) => {
    if (!req.headers.authorization) {
        return create();
    }
    const [type, token] = req.headers.authorization.split(' ');
    if (token && type === 'Token') {
        return get(token);
    }
    if (token && type === 'Bearer') {
        return check(token);
    }
    throw new AuthenticationError('Invalid authentication header!');
};