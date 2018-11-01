const { gql } = require('apollo-server');

types = gql` 

    """
    Get or create user authorization token
    """
    type UserIdentity {
        token: String!
    }
    
    """
    Get info on currently authorized user
    """    
    type UserInfo {
        token: String!
        is_loggedin: Boolean
        is_registered: Boolean
        accepted_privacy_policy: Boolean
        accepted_terms_of_service: Boolean   
        email: String
        first_name: String
        last_name: String 
    }
    
    """
    Get currently authorized user - available only for JWT authorized requests
    """    
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
        userInfo: UserInfo
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
        acceptPrivacyPolicy: UserInfo
        collectEmail(input: CollectEmailInput): UserInfo
        registerUser(input: RegisterUserInput): UserInfo
        loginUser(input: LoginUserInput): UserInfo
        logoutUser: UserIdentity
        updateUser(input: UpdateUserInput): UserInfo        
    }
`;

module.exports = types;