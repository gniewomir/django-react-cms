const { gql } = require('apollo-server');

types = gql` 

    type UserIdentity {
        identity_token: String!
        elevated_token: String
        jwt_token: String
        is_registered: Boolean
        accepted_privacy_policy: Boolean
        accepted_terms_of_service: Boolean
    }
    
    type User  {
        identity_token: String!
        elevated_token: String
        jwt_token: String
        is_registered: Boolean
        accepted_privacy_policy: Boolean
        accepted_terms_of_service: Boolean
        username: String
        email: String
        first_name: String
        last_name: String
    }
    
    type Query {
        userIdentity: UserIdentity
        user: User
    }
    
    input CollectEmailInput {
        email: String!
    }
            
    input RegisterUserInput {
        email: String!
        password: String!
        accepted_privacy_policy: Boolean!
        accepted_terms_of_service: Boolean!
        first_name: String
        last_name: String
    }

    input LoginUserInput {
        email: String!
        password: String!
    }
    
    input UpdateUserInput {
        email: String
        first_name: String
        last_name: String
        accepted_privacy_policy: Boolean
        accepted_terms_of_service: Boolean
    }
    
    type Mutation {
        acceptPrivacyPolicy: UserIdentity
        collectEmail(input: CollectEmailInput): UserIdentity
        registerUser(input: RegisterUserInput): UserIdentity
        loginUser(input: LoginUserInput): UserIdentity
        logoutUser: UserIdentity
        updateUser(input: UpdateUserInput): User        
    }
`;

module.exports = types;