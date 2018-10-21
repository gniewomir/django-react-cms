const {RESTDataSource} = require('apollo-datasource-rest');
const {services: {accounts}} = require('../config');

module.exports = class AccountsService extends RESTDataSource {
    constructor() {
        super();
        this.baseURL = accounts;
    }

    willSendRequest(request) {
        request.headers.set('Authorization', `Token ${this.context.token}`);
    }

    async createUser() {
        return this.post('users/')
    }

    async getUserByToken(token) {
        return this.get(`users/${token}`)
    }

    async getUserByUUID(uuid) {
        return this.get(`users/${uuid}`)
    }
};



