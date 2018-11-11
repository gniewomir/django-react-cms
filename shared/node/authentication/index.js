const jwt = require('jsonwebtoken');

const settings = {
    SERVICE_NAME: process.env.SERVICE_NAME,
    SERVICE_PERMISSIONS: process.env.SERVICE_PERMISSIONS,
    SECRET_KEY: process.env.SECRET_KEY,
    JWT_EXPIRATION: process.env.JWT_EXPIRATION,
    JWT_ALGORITHM: process.env.JWT_ALGORITHM,
};

const get_service_name = () => {
    return settings.SERVICE_NAME
};

const get_service_permission = (entity = null, method = null) => {
    return [get_service_name(), entity, method ? method.toUpperCase() : method].filter(element => !!element).join(':');
};

const get_current_service_permissions = () => {
    return settings.SERVICE_PERMISSIONS.split(',').map(perm => perm.trim())
};

const create_service_jwt_payload = () => {
    return {
        is_user: false,
        is_service: true,
        service_name: get_service_name(),
        service_permissions: get_current_service_permissions()
    }
};

const create_service_jwt = () => {
    return new Promise((resolve, reject) => {
        jwt.sign(
            create_service_jwt_payload(),
            settings.SECRET_KEY,
            {
                algorithm: settings.JWT_ALGORITHM,
                expiresIn: settings.JWT_EXPIRATION
            },
            (error, token) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(token);
            }
        );
    })
};

const validate_service_jwt = (token) => {
    return new Promise((resolve, reject) => {
        jwt.verify(
            token,
            settings.SECRET_KEY,
            {
                algorithms: [settings.JWT_ALGORITHM]
            },
            (error, decoded) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(decoded);
            }
        );
    })
};

module.exports = {
    create_service_jwt_payload,
    create_service_jwt,
    validate_service_jwt,
    get_service_name,
    get_service_permission,
    get_current_service_permissions,
};
