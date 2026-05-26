/**
 * sub - The SUB Hacking & Info Tool (Kotlin)
 * Author: Subhobhai (subhobhai943)
 * GitHub: https://github.com/subhobhai943
 */

import java.net.InetAddress
import java.net.Socket
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

val BANNER = """
  ███████╗██╗   ██╗██████╗ 
  ██╔════╝██║   ██║██╔══██╗
  ███████╗██║   ██║██████╔╝
  ╚════██║██║   ██║██╔══██╗
  ███████║╚██████╔╝██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ 
  by Subhobhai | github.com/subhobhai943
"""

fun banner() = println(BANNER)

fun whoami() {
    println(BANNER)
    val info = listOf(
        "Name"      to "Subhobhai Sarkar",
        "Alias"     to "sub",
        "GitHub"    to "https://github.com/subhobhai943",
        "Portfolio" to "https://sub-portofolio.netlify.app",
        "Location"  to "Durgapur, West Bengal, India",
        "Bio"       to "PCMB student | Web, AI, C++/C# game dev | Open-source hacker",
        "Projects"  to "AIOS, SUB lang, Discord bots, 3D web games",
        "Languages" to "Python, C, C++, Rust, Kotlin, Java, JS, Assembly"
    )
    for ((k, v) in info) println("  ${k.padEnd(12)}: $v")
    println()
}

fun sysInfo() {
    println("\n[*] System Information")
    val os   = System.getProperty("os.name") + " " + System.getProperty("os.version")
    val arch = System.getProperty("os.arch")
    val java = System.getProperty("java.version")
    val host = try { InetAddress.getLocalHost().hostName } catch (e: Exception) { "unknown" }
    val ip   = try { InetAddress.getLocalHost().hostAddress } catch (e: Exception) { "unknown" }
    val now  = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))
    println("  OS       : $os ($arch)")
    println("  Hostname : $host")
    println("  Local IP : $ip")
    println("  Java     : $java")
    println("  Time     : $now")
    println()
}

fun checkPorts(host: String) {
    val ports = listOf(21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5900, 8080, 8443)
    println("\n[*] Checking common ports on $host ...")
    for (port in ports) {
        try {
            val sock = Socket()
            sock.connect(java.net.InetSocketAddress(host, port), 500)
            sock.close()
            println("  Port ${port.toString().padEnd(6)}: OPEN")
        } catch (e: Exception) {
            println("  Port ${port.toString().padEnd(6)}: CLOSED")
        }
    }
    println()
}

fun printHelp() {
    println(BANNER)
    println("Usage: sub <command> [args]")
    println()
    println("Commands:")
    println("  banner            Show ASCII banner")
    println("  whoami            Author info")
    println("  info              System information")
    println("  ports <host>      Check common open ports")
    println()
    println("GitHub: https://github.com/subhobhai943")
}

fun main(args: Array<String>) {
    if (args.isEmpty()) { printHelp(); return }
    when (args[0]) {
        "banner" -> banner()
        "whoami" -> whoami()
        "info"   -> sysInfo()
        "ports"  -> if (args.size > 1) checkPorts(args[1]) else println("Usage: sub ports <host>")
        else     -> printHelp()
    }
}
