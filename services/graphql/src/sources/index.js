const AccountsService = require('./accounts.js');

module.exports = () => {
    return {
        AccountsService: new AccountsService()
    };
};
