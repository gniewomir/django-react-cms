const {RESTDataSource} = require('apollo-datasource-rest');
const {services: {accounts}} = require('../config');

module.exports = class AccountsService extends RESTDataSource {
    constructor() {
        super();
        this.baseURL = accounts;
    }

    willSendRequest(request) {
        request.headers.set('authorization', this.context.auth);
    }

    createUser() {
        return this.post('user/')
    }

    getCurrentUser() {
        return this.get(`user/${this.context.user.identity_token}/`)
    }

    getUserByUUID(uuid) {
        return this.get(`user/${uuid}/`)
    }

    update(args) {
        return this.patch(`user/${this.context.user.identity_token}/`, args)
    }

    login(args) {
        return this.post(`user/`, args)
    }

    logout() {
        return this.delete(`user/${this.context.user.identity_token}/`)
    }
};



