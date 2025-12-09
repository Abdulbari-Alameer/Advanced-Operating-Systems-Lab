/*
 * File: remote.x
 * Purpose: RPC interface definition for remote "who" command
 * 
 * This file defines:
 * - Data structures for communication
 * - Remote procedures
 * - Program number and version
 * 
 * Compilation:
 * rpcgen remote.x
 * This generates: remote.h, remote_clnt.c, remote_svc.c, remote_xdr.c
 */

/* Maximum length for user information string */
const MAX_INFO_LEN = 1024;
const MAX_USERS = 100;

/* Structure to hold single user information */
struct user_info {
    char username[32];
    char terminal[32];
    char hostname[256];
    char logintime[64];
};

/* Structure to hold all logged-in users */
struct user_list {
    user_info users<MAX_USERS>;  /* Variable-length array */
    int count;                   /* Number of users */
};

/* RPC Program Definition */
program REMOTE_PROG {
    version REMOTE_VERS {
        /* Remote procedure to get logged-in users */
        user_list GET_LOGGED_USERS(void) = 1;
        
        /* Alternative: return simple string format */
        string GET_USERS_STRING(void) = 2;
    } = 1;  /* Version number */
} = 0x20000001;  /* Program number (must be unique) */

/*
 * EXPLANATION:
 * 
 * 1. Program Number (0x20000001):
 *    - Must be in range 0x20000000 - 0x3fffffff for user programs
 *    - Uniquely identifies this RPC service
 * 
 * 2. Version Number (1):
 *    - Allows multiple versions of same program
 *    - Enables backward compatibility
 * 
 * 3. Procedure Numbers:
 *    - GET_LOGGED_USERS = 1
 *    - GET_USERS_STRING = 2
 *    - Procedure 0 is reserved for NULL procedure
 * 
 * 4. rpcgen generates:
 *    - remote.h: Header with definitions
 *    - remote_clnt.c: Client stub
 *    - remote_svc.c: Server stub
 *    - remote_xdr.c: XDR routines for data serialization
 */