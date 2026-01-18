# JWT Configuration Guide

This document outlines the JWT (JSON Web Token) configuration for the application.

## Overview

The application uses JWT tokens for authentication and authorization. The configuration includes both frontend and backend components using the `better-auth` library.

## Backend Configuration (`backend/app/core/security.py`)

### JWT Settings
- **Algorithm**: HS256
- **Secret Key**: Stored in environment variable `BETTER_AUTH_SECRET`
- **Token Expiration**: 24 hours (1440 minutes)
- **Libraries Used**: `python-jose`, `passlib`

### Key Functions
- `create_access_token()`: Creates new JWT tokens with expiration
- `verify_token()`: Validates JWT tokens and extracts user information
- `get_current_user()`: FastAPI dependency to extract current user from token

## Frontend Configuration (`frontend/src/lib/auth-client.ts`)

### JWT Plugin Settings
- **Header**: Authorization
- **Prefix**: Bearer
- **Cookie**: auth-token

### Configuration Example
```typescript
import { createAuthClient } from 'better-auth/client';
import { jwtPlugin } from 'better-auth/client/plugins';

export const authClient = createAuthClient({
  plugins: [
    jwtPlugin({
      header: 'Authorization',
      prefix: 'Bearer ',
      cookie: 'auth-token',
    })
  ]
});
```

## Security Considerations

- The secret key should be strong and kept secure
- For production, ensure the secret is stored securely (not hardcoded)
- Tokens expire after 24 hours to limit exposure windows
- All API endpoints require valid JWT tokens for access

## Environment Variables

- `BETTER_AUTH_SECRET`: Secret key used for signing JWT tokens
- Ensure this is set appropriately for each environment (development, staging, production)