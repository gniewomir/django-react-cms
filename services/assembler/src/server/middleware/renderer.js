import React from "react";
import Server from '../../scene/Server';
import document from '../../scene/Document';

export const createRendererMiddleware = () => {
    return async (req, res, next) => {
        const context = {
            client: res.locals.client
        };
        const response = await document(Server(context, req.url), context);
        res.status(200);
        res.send(response);
        res.end()
    }
};
