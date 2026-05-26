/**
 * sub - The SUB Hacking & Info Tool (Java)
 * Author: Subhobhai (subhobhai943)
 * GitHub: https://github.com/subhobhai943
 */

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Sub {

    static final String BANNER =
        "\n  ███████╗██╗   ██╗██████╗ \n" +
        "  ██╔════╝██║   ██║██╔══██╗\n" +
        "  ███████╗██║   ██║██████╔╝\n" +
        "  ╚════██║██║   ██║██╔══██╗\n" +
        "  ███████║╚██████╔╝██████╔╝\n" +
        "  ╚══════╝ ╚═════╝ ╚═════╝ \n" +
        "  by Subhobhai | github.com/subhobhai943\n";

    static void banner() {
        System.out.println(BANNER);
    }

    static void whoami() {
        System.out.println(BANNER);
        String[][] info = {
            {"Name",      "Subhobhai Sarkar"},
            {"Alias",     "sub"},
            {"GitHub",    "https://github.com/subhobhai943"},
            {"Portfolio", "https://sub-portofolio.netlify.app"},
            {"Location",  "Durgapur, West Bengal, India"},
            {"Bio",       "PCMB student | Web, AI, C++/C# game dev | Open-source hacker"},
            {"Projects",  "AIOS, SUB lang, Discord bots, 3D web games"},
            {"Languages", "Python, C, C++, Rust, Kotlin, Java, JS, Assembly"}
        };
        for (String[] row : info) {
            System.out.printf("  %-12s: %s%n", row[0], row[1]);
        }
        System.out.println();
    }

    static void sysInfo() {
        System.out.println("\n[*] System Information");
        String os   = System.getProperty("os.name") + " " + System.getProperty("os.version");
        String arch = System.getProperty("os.arch");
        String java = System.getProperty("java.version");
        String host, ip;
        try {
            host = InetAddress.getLocalHost().getHostName();
            ip   = InetAddress.getLocalHost().getHostAddress();
        } catch (Exception e) {
            host = "unknown"; ip = "unknown";
        }
        String now = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        System.out.printf("  OS       : %s (%s)%n", os, arch);
        System.out.printf("  Hostname : %s%n", host);
        System.out.printf("  Local IP : %s%n", ip);
        System.out.printf("  Java     : %s%n", java);
        System.out.printf("  Time     : %s%n", now);
        System.out.println();
    }

    static void checkPorts(String host) {
        int[] ports = {21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5900, 8080, 8443};
        System.out.println("\n[*] Checking common ports on " + host + " ...");
        for (int port : ports) {
            try (Socket sock = new Socket()) {
                sock.connect(new InetSocketAddress(host, port), 500);
                System.out.printf("  Port %-6d: OPEN%n", port);
            } catch (Exception e) {
                System.out.printf("  Port %-6d: CLOSED%n", port);
            }
        }
        System.out.println();
    }

    static void printHelp() {
        System.out.println(BANNER);
        System.out.println("Usage: sub <command> [args]");
        System.out.println();
        System.out.println("Commands:");
        System.out.println("  banner            Show ASCII banner");
        System.out.println("  whoami            Author info");
        System.out.println("  info              System information");
        System.out.println("  ports <host>      Check common open ports");
        System.out.println();
        System.out.println("GitHub: https://github.com/subhobhai943");
    }

    public static void main(String[] args) {
        if (args.length == 0) { printHelp(); return; }
        switch (args[0]) {
            case "banner" -> banner();
            case "whoami" -> whoami();
            case "info"   -> sysInfo();
            case "ports"  -> {
                if (args.length > 1) checkPorts(args[1]);
                else System.out.println("Usage: sub ports <host>");
            }
            default -> printHelp();
        }
    }
}
