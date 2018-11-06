import React from 'react';
import express from 'express';
import {createAuthorizationMiddleware} from './server/middleware/authorization';
import {createRendererMiddleware} from './server/middleware/renderer';
import createCookieParser from 'cookie-parser';
const server = express();

server
    .use(express.static(process.env.RAZZLE_PUBLIC_DIR))
    .use(createCookieParser())
    .use(createAuthorizationMiddleware())
    .get('/*', createRendererMiddleware());

export default server;