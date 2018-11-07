import gql from "graphql-tag";
import {Query} from "react-apollo";
import React from 'react';

export default () => (
    <Query query={gql`
                    query {
                      userIdentity {
                        token
                      }
                    }
           `}
           pollInterval={500000}
    >
        {({loading, error, data}) => {
            if (loading) return null;
            if (error) return `Error! ${error.message}`;
            return (
                <pre>
                    {JSON.stringify(data)}
                </pre>
            );
        }}
    </Query>
);