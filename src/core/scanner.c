/*
 * scanner.c — Fast TCP port scanner for SUB
 * Author : Subhobhai (subhobhai943)
 * Compile: gcc -O2 -o sub-scan scanner.c
 * Usage  : sub-scan <host> [start_port] [end_port]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <errno.h>

#define DEFAULT_START  1
#define DEFAULT_END    1024
#define TIMEOUT_SEC    1
#define MAX_BANNER     256

/* ANSI colors */
#define RED    "\033[91m"
#define GREEN  "\033[92m"
#define YELLOW "\033[93m"
#define CYAN   "\033[96m"
#define WHITE  "\033[97m"
#define BOLD   "\033[1m"
#define RESET  "\033[0m"

/* Resolve hostname to IP string */
int resolve(const char *host, char *ip_out) {
    struct addrinfo hints, *res;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    if (getaddrinfo(host, NULL, &hints, &res) != 0) return -1;
    struct sockaddr_in *addr = (struct sockaddr_in *)res->ai_addr;
    inet_ntop(AF_INET, &addr->sin_addr, ip_out, INET_ADDRSTRLEN);
    freeaddrinfo(res);
    return 0;
}

/* Try to grab service banner */
void grab_banner(const char *ip, int port, char *banner_out) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return;
    struct timeval tv = {1, 0};
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    struct sockaddr_in sa;
    sa.sin_family = AF_INET;
    sa.sin_port = htons(port);
    inet_pton(AF_INET, ip, &sa.sin_addr);
    if (connect(sock, (struct sockaddr *)&sa, sizeof(sa)) == 0) {
        /* Send HTTP probe for port 80/443/8080, else generic */
        if (port == 80 || port == 8080 || port == 443) {
            send(sock, "HEAD / HTTP/1.0\r\n\r\n", 20, 0);
        }
        int n = recv(sock, banner_out, MAX_BANNER - 1, 0);
        if (n > 0) {
            banner_out[n] = '\0';
            /* Replace newlines for clean output */
            for (int i = 0; i < n; i++)
                if (banner_out[i] == '\n' || banner_out[i] == '\r')
                    banner_out[i] = ' ';
        }
    }
    close(sock);
}

/* Non-blocking connect with timeout */
int scan_port(const char *ip, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return 0;

    /* Set non-blocking */
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);

    struct sockaddr_in sa;
    memset(&sa, 0, sizeof(sa));
    sa.sin_family = AF_INET;
    sa.sin_port   = htons(port);
    inet_pton(AF_INET, ip, &sa.sin_addr);

    int result = connect(sock, (struct sockaddr *)&sa, sizeof(sa));
    int open = 0;

    if (result == 0) {
        open = 1;
    } else if (errno == EINPROGRESS) {
        fd_set wfds;
        FD_ZERO(&wfds);
        FD_SET(sock, &wfds);
        struct timeval tv = {TIMEOUT_SEC, 0};
        if (select(sock + 1, NULL, &wfds, NULL, &tv) > 0) {
            int err = 0; socklen_t len = sizeof(err);
            getsockopt(sock, SOL_SOCKET, SO_ERROR, &err, &len);
            open = (err == 0);
        }
    }
    close(sock);
    return open;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: sub-scan <host> [start_port] [end_port]\n");
        return 1;
    }

    const char *host  = argv[1];
    int start = (argc >= 3) ? atoi(argv[2]) : DEFAULT_START;
    int end   = (argc >= 4) ? atoi(argv[3]) : DEFAULT_END;

    char ip[INET_ADDRSTRLEN] = {0};
    if (resolve(host, ip) != 0) {
        fprintf(stderr, RED "[!] Could not resolve: %s\n" RESET, host);
        return 1;
    }

    printf("\n" CYAN BOLD "[SUB-SCAN] Target: " YELLOW "%s" WHITE " (" GREEN "%s" WHITE ")" RESET "\n", host, ip);
    printf(CYAN "[SUB-SCAN] Range : " YELLOW "%d" WHITE " - " YELLOW "%d" RESET "\n\n", start, end);

    int found = 0;
    for (int port = start; port <= end; port++) {
        if (scan_port(ip, port)) {
            char banner[MAX_BANNER] = {0};
            grab_banner(ip, port, banner);
            printf("  " GREEN "[OPEN]" WHITE "  Port " YELLOW "%-6d" RESET, port);
            if (strlen(banner) > 0) {
                /* Truncate banner to 60 chars */
                char short_banner[61] = {0};
                strncpy(short_banner, banner, 60);
                printf(" | " CYAN "%s" RESET, short_banner);
            }
            printf("\n");
            found++;
        }
    }

    if (found == 0)
        printf("  " RED "[!] No open ports found in range %d-%d" RESET "\n", start, end);
    else
        printf("\n  " GREEN "[+] %d open port(s) found." RESET "\n", found);

    printf("\n");
    return 0;
}
