// OsintTools.java — Java OSINT module for SUB
// Author : Subhobhai (subhobhai943)
// Compile: javac OsintTools.java && jar cfe sub-osint.jar OsintTools *.class
// Usage  : java -jar sub-osint.jar <command> [args]

import java.net.*;
import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.nio.charset.StandardCharsets;

public class OsintTools {

    // ── ANSI
    static final String R   = "\u001b[91m";
    static final String G   = "\u001b[92m";
    static final String Y   = "\u001b[93m";
    static final String C   = "\u001b[96m";
    static final String W   = "\u001b[97m";
    static final String BD  = "\u001b[1m";
    static final String RST = "\u001b[0m";

    static void banner() {
        System.out.println(
            "\n" + C + BD + "  [SUB-OSINT] Java OSINT Module v1.0.0" + RST +
            "\n  " + Y + "By Subhobhai (subhobhai943)" + RST +
            "\n  " + W + "https://github.com/subhobhai943" + RST + "\n"
        );
    }

    // ── HTTP GET helper
    static String httpGet(String urlStr, int timeout) throws Exception {
        URL url = new URL(urlStr);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setConnectTimeout(timeout);
        conn.setReadTimeout(timeout);
        conn.setRequestProperty("User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64) SUB-OSINT/1.0");
        int code = conn.getResponseCode();
        InputStream is = (code >= 400) ? conn.getErrorStream() : conn.getInputStream();
        if (is == null) return "";
        BufferedReader rd = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = rd.readLine()) != null) sb.append(line).append("\n");
        conn.disconnect();
        return sb.toString();
    }

    // ── Simple JSON field extractor
    static String jsonGet(String json, String key) {
        Pattern p = Pattern.compile("\"" + key + "\"\\s*:\\s*\"?([^\"\\}\\],]+)\"?");
        Matcher m = p.matcher(json);
        return m.find() ? m.group(1).trim() : "N/A";
    }

    // ── 1. IP Geolocation
    static void cmdGeoip(String ip) {
        System.out.println("\n" + C + "[*]" + W + " GeoIP: " + Y + ip + RST + "\n");
        try {
            String json = httpGet("http://ip-api.com/json/" + ip +
                "?fields=status,country,regionName,city,zip,lat,lon,isp,org,as,query", 5000);
            System.out.println("  " + Y + "IP          " + W + ": " + G + jsonGet(json, "query") + RST);
            System.out.println("  " + Y + "Country     " + W + ": " + G + jsonGet(json, "country") + RST);
            System.out.println("  " + Y + "Region      " + W + ": " + G + jsonGet(json, "regionName") + RST);
            System.out.println("  " + Y + "City        " + W + ": " + G + jsonGet(json, "city") + RST);
            System.out.println("  " + Y + "ZIP         " + W + ": " + G + jsonGet(json, "zip") + RST);
            System.out.println("  " + Y + "Lat/Lon     " + W + ": " + G +
                jsonGet(json, "lat") + ", " + jsonGet(json, "lon") + RST);
            System.out.println("  " + Y + "ISP         " + W + ": " + G + jsonGet(json, "isp") + RST);
            System.out.println("  " + Y + "Org         " + W + ": " + G + jsonGet(json, "org") + RST);
            System.out.println("  " + Y + "AS          " + W + ": " + G + jsonGet(json, "as") + RST);
        } catch (Exception e) {
            System.out.println("  " + R + "[!] " + e.getMessage() + RST);
        }
        System.out.println();
    }

    // ── 2. Email header analyser
    static void cmdEmailHeader(String filePath) {
        System.out.println("\n" + C + "[*]" + W + " Analysing email headers from: " + Y + filePath + RST + "\n");
        try {
            List<String> lines = new ArrayList<>();
            BufferedReader br = new BufferedReader(new FileReader(filePath));
            String line;
            while ((line = br.readLine()) != null) lines.add(line);
            br.close();

            Map<String, String> fields = new LinkedHashMap<>();
            String[] keys = {"From", "To", "Subject", "Date", "Message-ID",
                             "X-Mailer", "X-Originating-IP", "Received",
                             "Return-Path", "Reply-To", "DKIM-Signature"};

            for (String k : keys) {
                for (String l : lines) {
                    if (l.toLowerCase().startsWith(k.toLowerCase() + ":")) {
                        fields.put(k, l.substring(k.length() + 1).trim());
                        break;
                    }
                }
            }

            if (fields.isEmpty()) {
                System.out.println("  " + R + "[!] No recognised email header fields found." + RST);
            } else {
                fields.forEach((k, v) ->
                    System.out.printf("  " + Y + "%-20s" + W + ": " + G + "%s" + RST + "%n", k, v));
            }

            // Look for IPs in Received headers
            System.out.println("\n  " + C + "[IPs found in headers:]" + RST);
            Pattern ipPat = Pattern.compile("\\b(\\d{1,3}\\.){3}\\d{1,3}\\b");
            Set<String> ips = new LinkedHashSet<>();
            for (String l : lines) {
                Matcher m = ipPat.matcher(l);
                while (m.find()) ips.add(m.group());
            }
            if (ips.isEmpty()) {
                System.out.println("  " + Y + "  None found." + RST);
            } else {
                ips.forEach(ip -> System.out.println("  " + G + "  " + ip + RST));
            }
        } catch (Exception e) {
            System.out.println("  " + R + "[!] " + e.getMessage() + RST);
        }
        System.out.println();
    }

    // ── 3. Username search (generates search URLs)
    static void cmdUsername(String username) {
        System.out.println("\n" + C + "[*]" + W + " Username search: " + Y + username + RST + "\n");
        String[][] platforms = {
            {"GitHub",     "https://github.com/" + username},
            {"Twitter/X",  "https://twitter.com/" + username},
            {"Instagram",  "https://instagram.com/" + username},
            {"Reddit",     "https://reddit.com/user/" + username},
            {"TikTok",     "https://tiktok.com/@" + username},
            {"YouTube",    "https://youtube.com/@" + username},
            {"LinkedIn",   "https://linkedin.com/in/" + username},
            {"HackerNews", "https://news.ycombinator.com/user?id=" + username},
            {"Dev.to",     "https://dev.to/" + username},
            {"Replit",     "https://replit.com/@" + username},
            {"Gitlab",     "https://gitlab.com/" + username},
            {"Pastebin",   "https://pastebin.com/u/" + username},
        };
        for (String[] p : platforms) {
            // Quick HTTP check
            String status = "";
            try {
                URL url = new URL(p[1]);
                HttpURLConnection c = (HttpURLConnection) url.openConnection();
                c.setRequestMethod("HEAD");
                c.setConnectTimeout(2000);
                c.setReadTimeout(2000);
                c.setRequestProperty("User-Agent", "Mozilla/5.0 SUB-OSINT");
                c.setInstanceFollowRedirects(true);
                int code = c.getResponseCode();
                status = (code == 200) ? G + "[FOUND]" + RST : Y + "[" + code + "]" + RST;
                c.disconnect();
            } catch (Exception e) {
                status = R + "[ERR]" + RST;
            }
            System.out.printf("  %-10s %s  %s%s%s%n", status, C, p[1], RST, "");
        }
        System.out.println();
    }

    // ── 4. URL expander (follow redirects)
    static void cmdExpandUrl(String shortUrl) {
        System.out.println("\n" + C + "[*]" + W + " Expanding: " + Y + shortUrl + RST + "\n");
        try {
            URL url = new URL(shortUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setInstanceFollowRedirects(false);
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 SUB-OSINT");
            conn.connect();

            int step = 0;
            String current = shortUrl;
            while (true) {
                int code = conn.getResponseCode();
                System.out.printf("  " + Y + "Step %-2d" + W + ": [%d] " + G + "%s" + RST + "%n", step, code, current);
                if (code / 100 != 3) break;
                String loc = conn.getHeaderField("Location");
                if (loc == null) break;
                current = loc;
                conn.disconnect();
                url = new URL(current);
                conn = (HttpURLConnection) url.openConnection();
                conn.setInstanceFollowRedirects(false);
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                conn.setRequestProperty("User-Agent", "Mozilla/5.0 SUB-OSINT");
                conn.connect();
                step++;
                if (step > 10) { System.out.println("  " + R + "[!] Too many redirects." + RST); break; }
            }
            conn.disconnect();
        } catch (Exception e) {
            System.out.println("  " + R + "[!] " + e.getMessage() + RST);
        }
        System.out.println();
    }

    // ── 5. HTTP status checker (batch)
    static void cmdHttpStatus(String url) {
        System.out.println("\n" + C + "[*]" + W + " HTTP status: " + Y + url + RST + "\n");
        try {
            if (!url.startsWith("http")) url = "https://" + url;
            HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 SUB-OSINT");
            int code = conn.getResponseCode();
            String msg  = conn.getResponseMessage();
            String server = conn.getHeaderField("Server");
            String powered = conn.getHeaderField("X-Powered-By");
            String ct = conn.getHeaderField("Content-Type");
            System.out.println("  " + Y + "Status       " + W + ": " + (code < 400 ? G : R) + code + " " + msg + RST);
            if (server  != null) System.out.println("  " + Y + "Server       " + W + ": " + G + server + RST);
            if (powered != null) System.out.println("  " + Y + "X-Powered-By " + W + ": " + G + powered + RST);
            if (ct      != null) System.out.println("  " + Y + "Content-Type " + W + ": " + G + ct + RST);
            conn.disconnect();
        } catch (Exception e) {
            System.out.println("  " + R + "[!] " + e.getMessage() + RST);
        }
        System.out.println();
    }

    // ── Main
    public static void main(String[] args) {
        banner();
        if (args.length == 0) {
            System.out.println(Y + "Commands:" + RST);
            System.out.println("  " + C + "geoip     <ip>           " + W + "IP geolocation");
            System.out.println("  " + C + "email     <file>         " + W + "Email header analysis");
            System.out.println("  " + C + "username  <name>         " + W + "Username presence check");
            System.out.println("  " + C + "expand    <url>          " + W + "Expand/follow shortened URLs");
            System.out.println("  " + C + "httpstat  <url>          " + W + "HTTP status + server fingerprint\n");
            return;
        }
        switch (args[0]) {
            case "geoip"    -> { if (args.length < 2) err("geoip <ip>");          else cmdGeoip(args[1]); }
            case "email"    -> { if (args.length < 2) err("email <file>");        else cmdEmailHeader(args[1]); }
            case "username" -> { if (args.length < 2) err("username <name>");     else cmdUsername(args[1]); }
            case "expand"   -> { if (args.length < 2) err("expand <url>");        else cmdExpandUrl(args[1]); }
            case "httpstat" -> { if (args.length < 2) err("httpstat <url>");      else cmdHttpStatus(args[1]); }
            default         -> System.out.println(R + "[!] Unknown: " + args[0] + RST);
        }
    }

    static void err(String usage) {
        System.out.println(R + "Usage: sub-osint " + usage + RST);
    }
}
