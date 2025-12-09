#include <stdio.h>
#include <stdlib.h>
#include <utmp.h>
#include <string.h>
#include <time.h>

/*
 * Program: local_who.c
 * Purpose: Display logged-in users by reading /var/run/utmp
 * Compilation: gcc -o local_who local_who.c
 * Usage: ./local_who
 */

#define UTMP_FILE "/var/run/utmp"

void display_user_info(struct utmp *ut_entry) {
    char time_str[100];
    time_t login_time;
    
    // Convert login time to readable format
    login_time = ut_entry->ut_time;
    struct tm *tm_info = localtime(&login_time);
    strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M", tm_info);
    
    // Print user information
    printf("%-10s %-10s %-16s %s\n", 
           ut_entry->ut_user,           // Username
           ut_entry->ut_line,           // Terminal line
           ut_entry->ut_host,           // Remote host
           time_str);                   // Login time
}

int main() {
    FILE *utmp_file;
    struct utmp ut_entry;
    
    printf("Currently logged-in users:\n");
    printf("%-10s %-10s %-16s %s\n", "USER", "TTY", "FROM", "LOGIN@");
    printf("================================================================\n");
    
    // Open the utmp file
    utmp_file = fopen(UTMP_FILE, "rb");
    if (utmp_file == NULL) {
        perror("Error opening utmp file");
        exit(EXIT_FAILURE);
    }
    
    // Read and process each utmp entry
    while (fread(&ut_entry, sizeof(struct utmp), 1, utmp_file) == 1) {
        // Only display USER_PROCESS entries (actual logged-in users)
        if (ut_entry.ut_type == USER_PROCESS) {
            display_user_info(&ut_entry);
        }
    }
    
    // Close the file
    if (fclose(utmp_file) != 0) {
        perror("Error closing utmp file");
        exit(EXIT_FAILURE);
    }
    
    return 0;
}

/*
 * EXPLANATION OF KEY CONCEPTS:
 * 
 * 1. /var/run/utmp file:
 *    - Binary file containing current login records
 *    - Each record is a 'struct utmp'
 *    - Updated by login/init processes
 * 
 * 2. struct utmp members (important ones):
 *    - ut_type: Type of record (USER_PROCESS for logged-in users)
 *    - ut_user: Username of logged-in user
 *    - ut_line: Device name (terminal)
 *    - ut_host: Remote hostname (if applicable)
 *    - ut_time: Login timestamp
 * 
 * 3. fopen() usage:
 *    - Opens file in binary read mode ("rb")
 *    - Returns FILE pointer or NULL on error
 * 
 * 4. fread() usage:
 *    - Reads binary data from file
 *    - Returns number of items successfully read
 */