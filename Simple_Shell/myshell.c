#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAX_CMD 100

// Trim newline and extra spaces
void trim(char *str) {
    int len = strlen(str);

    // Remove newline
    if (len > 0 && str[len - 1] == '\n')
        str[len - 1] = '\0';

    // Remove trailing spaces
    for (int i = strlen(str) - 1; i >= 0 && str[i] == ' '; i--) {
        str[i] = '\0';
    }
}

int main() {
    char command[MAX_CMD];

    while (1) {
        printf("%% ");      // Shell prompt

        if (fgets(command, sizeof(command), stdin) == NULL) {
            printf("\nExiting shell...\n");
            break;         // Ctrl+D
        }

        trim(command);

        // Ignore empty commands
        if (strlen(command) == 0) {
            continue;
        }

        pid_t pid = fork();

        if (pid < 0) {
            perror("fork failed");
            continue;
        }

        if (pid == 0) {
            // Child executes command with execv()
            char *args[] = { "/bin/sh", "-c", command, NULL };

            execv("/bin/sh", args);

            // Only runs if execv() fails
            perror("execv failed");
            _exit(1);
        }

        else {
            // Parent waits
            wait(NULL);
        }
    }

    return 0;
}