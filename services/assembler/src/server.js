import React from 'react';
import express from 'express';
import {createUpdateAuthCookieMiddleware, createAuthorizationMiddleware} from './server/middleware/authorization';
import {createRendererMiddleware} from './server/middleware/renderer';
import createCookieParser from 'cookie-parser';

const server = express();

server
    .use(express.static(process.env.RAZZLE_PUBLIC_DIR))
    .use(express.static(process.env.BUILD_DIR))
    .use(createCookieParser())
    .get('/update-cookie', createUpdateAuthCookieMiddleware())
    .use(createAuthorizationMiddleware())
    .get('/*', createRendererMiddleware());

export default server;