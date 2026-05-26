// NetUtils.kt — Kotlin network utilities module for SUB
// Author : Subhobhai (subhobhai943)
// Compile: kotlinc NetUtils.kt -include-runtime -d sub-net.jar
// Usage  : java -jar sub-net.jar <command> [args]

import java.net.*
import java.io.*
import java.util.concurrent.*
import java.util.concurrent.atomic.AtomicInteger

// ── ANSI
const val R   = "\u001b[91m"
const val G   = "\u001b[92m"
const val Y   = "\u001b[93m"
const val C   = "\u001b[96m"
const val W   = "\u001b[97m"
const val BD  = "\u001b[1m"
const val RST = "\u001b[0m"

fun banner() {
    println("""
${C}${BD}  [SUB-NET] Kotlin Network Module v1.0.0${RST}
  ${Y}By Subhobhai (subhobhai943)${RST}
  ${W}https://github.com/subhobhai943${RST}
""")
}

// ── Threaded port scanner
fun cmdScan(host: String, startPort: Int, endPort: Int, threads: Int = 100) {
    println("\n${C}[*]${W} Threaded Kotlin port scan: ${Y}$host${W} ports ${Y}$startPort-$endPort${RST}")
    println("${C}[*]${W} Threads: ${Y}$threads${RST}\n")

    val executor = Executors.newFixedThreadPool(threads)
    val openPorts = ConcurrentLinkedQueue<Int>()
    val latch = CountDownLatch(endPort - startPort + 1)

    for (port in startPort..endPort) {
        executor.submit {
            try {
                val sock = Socket()
                sock.connect(InetSocketAddress(host, port), 400)
                openPorts.add(port)
                sock.close()
            } catch (_: Exception) {}
            latch.countDown()
        }
    }

    latch.await(30, TimeUnit.SECONDS)
    executor.shutdownNow()

    if (openPorts.isEmpty()) {
        println("  ${R}[!] No open ports found.${RST}")
    } else {
        openPorts.sorted().forEach { port ->
            println("  ${G}[OPEN]${W}  Port ${Y}$port${RST}")
        }
        println("\n  ${G}[+] ${openPorts.size} open port(s) found.${RST}")
    }
    println()
}

// ── Reverse DNS lookup
fun cmdReverseDns(ip: String) {
    println("\n${C}[*]${W} Reverse DNS for: ${Y}$ip${RST}\n")
    try {
        val addr = InetAddress.getByName(ip)
        val hostname = addr.canonicalHostName
        println("  ${Y}IP       ${W}: ${G}$ip${RST}")
        println("  ${Y}Hostname ${W}: ${G}$hostname${RST}\n")
    } catch (e: Exception) {
        println("  ${R}[!] Error: ${e.message}${RST}\n")
    }
}

// ── TCP banner grab
fun cmdBanner(host: String, port: Int) {
    println("\n${C}[*]${W} Banner grab: ${Y}$host:$port${RST}\n")
    try {
        val sock = Socket()
        sock.connect(InetSocketAddress(host, port), 3000)
        sock.soTimeout = 2000

        val writer = PrintWriter(sock.getOutputStream(), true)
        val reader = BufferedReader(InputStreamReader(sock.getInputStream()))

        // Send HTTP probe for web ports
        if (port == 80 || port == 8080 || port == 443) {
            writer.println("HEAD / HTTP/1.0\r\n")
        }

        val lines = mutableListOf<String>()
        try {
            var line = reader.readLine()
            while (line != null && lines.size < 10) {
                lines.add(line)
                line = reader.readLine()
            }
        } catch (_: Exception) {}

        sock.close()

        if (lines.isEmpty()) {
            println("  ${Y}[~] No banner received.${RST}")
        } else {
            lines.forEach { println("  ${G}>${W} $it${RST}") }
        }
    } catch (e: Exception) {
        println("  ${R}[!] Could not connect: ${e.message}${RST}")
    }
    println()
}

// ── Traceroute wrapper
fun cmdTraceroute(host: String) {
    println("\n${C}[*]${W} Traceroute to: ${Y}$host${RST}\n")
    try {
        val proc = ProcessBuilder("traceroute", "-n", "-m", "20", host)
            .redirectErrorStream(true)
            .start()
        val reader = BufferedReader(InputStreamReader(proc.inputStream))
        var line = reader.readLine()
        while (line != null) {
            println("  ${W}$line${RST}")
            line = reader.readLine()
        }
        proc.waitFor()
    } catch (e: Exception) {
        println("  ${R}[!] Error: ${e.message}${RST}")
        println("  ${Y}[*] Install: sudo apt install traceroute${RST}")
    }
    println()
}

// ── IP geolocation (ip-api.com — free, no key needed)
fun cmdGeoip(ip: String) {
    println("\n${C}[*]${W} GeoIP lookup: ${Y}$ip${RST}\n")
    try {
        val url = URL("http://ip-api.com/json/$ip?fields=status,country,regionName,city,isp,org,as,query")
        val conn = url.openConnection() as HttpURLConnection
        conn.connectTimeout = 5000
        conn.readTimeout    = 5000
        conn.requestMethod  = "GET"
        val response = conn.inputStream.bufferedReader().readText()
        conn.disconnect()

        // Simple JSON field extractor (no external lib needed)
        fun extract(json: String, key: String): String {
            val pattern = Regex("\"$key\":\"?([^\"\\},]+)\"?")
            return pattern.find(json)?.groupValues?.get(1)?.trim() ?: "N/A"
        }

        println("  ${Y}IP          ${W}: ${G}${extract(response, "query")}${RST}")
        println("  ${Y}Country     ${W}: ${G}${extract(response, "country")}${RST}")
        println("  ${Y}Region      ${W}: ${G}${extract(response, "regionName")}${RST}")
        println("  ${Y}City        ${W}: ${G}${extract(response, "city")}${RST}")
        println("  ${Y}ISP         ${W}: ${G}${extract(response, "isp")}${RST}")
        println("  ${Y}Org         ${W}: ${G}${extract(response, "org")}${RST}")
        println("  ${Y}AS          ${W}: ${G}${extract(response, "as")}${RST}")
    } catch (e: Exception) {
        println("  ${R}[!] Error: ${e.message}${RST}")
    }
    println()
}

// ── Network interfaces
fun cmdInterfaces() {
    println("\n${C}[*]${W} Network Interfaces${RST}\n")
    try {
        val interfaces = NetworkInterface.getNetworkInterfaces()
        interfaces?.toList()?.filter { it.isUp }?.forEach { iface ->
            println("  ${Y}${iface.displayName}${RST}")
            iface.inetAddresses.toList().forEach { addr ->
                val type = if (addr is Inet6Address) "IPv6" else "IPv4"
                println("    ${G}[$type]${W} ${addr.hostAddress}${RST}")
            }
        }
    } catch (e: Exception) {
        println("  ${R}[!] ${e.message}${RST}")
    }
    println()
}

// ── Main
fun main(args: Array<String>) {
    banner()

    if (args.isEmpty()) {
        println("${Y}Commands:${RST}")
        println("  ${C}scan      <host> <startPort> <endPort> [threads]  ${W}Threaded port scan")
        println("  ${C}rdns      <ip>                                    ${W}Reverse DNS lookup")
        println("  ${C}banner    <host> <port>                           ${W}TCP banner grab")
        println("  ${C}traceroute <host>                                  ${W}Traceroute")
        println("  ${C}geoip     <ip>                                    ${W}IP geolocation")
        println("  ${C}ifaces                                            ${W}Network interfaces\n")
        return
    }

    when (args[0]) {
        "scan"       -> {
            if (args.size < 4) { println("${R}Usage: sub-net scan <host> <start> <end> [threads]${RST}"); return }
            val threads = if (args.size >= 5) args[4].toIntOrNull() ?: 100 else 100
            cmdScan(args[1], args[2].toInt(), args[3].toInt(), threads)
        }
        "rdns"       -> { if (args.size < 2) { println("${R}Usage: sub-net rdns <ip>${RST}"); return }; cmdReverseDns(args[1]) }
        "banner"     -> { if (args.size < 3) { println("${R}Usage: sub-net banner <host> <port>${RST}"); return }; cmdBanner(args[1], args[2].toInt()) }
        "traceroute" -> { if (args.size < 2) { println("${R}Usage: sub-net traceroute <host>${RST}"); return }; cmdTraceroute(args[1]) }
        "geoip"      -> { if (args.size < 2) { println("${R}Usage: sub-net geoip <ip>${RST}"); return }; cmdGeoip(args[1]) }
        "ifaces"     -> cmdInterfaces()
        else         -> println("${R}[!] Unknown command: ${args[0]}${RST}")
    }
}
