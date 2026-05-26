// recon.rs — Rust recon & crypto tools for SUB
// Author : Subhobhai (subhobhai943)
// Compile: rustc -O -o sub-recon recon.rs
// Usage  : sub-recon <command> [args]

use std::env;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::net::TcpStream;
use std::time::Duration;

// ── ANSI ──────────────────────────────────────────────────
const R: &str = "\x1b[91m";
const G: &str = "\x1b[92m";
const Y: &str = "\x1b[93m";
const C: &str = "\x1b[96m";
const W: &str = "\x1b[97m";
const B: &str = "\x1b[1m";
const RST: &str = "\x1b[0m";

fn banner() {
    println!("\n{}{}[SUB-RECON]{} Rust Recon Engine v1.0.0 — by subhobhai943{}\n", C, B, W, RST);
}

// ── Hash identifier ───────────────────────────────────────
fn identify_hash(hash: &str) -> &'static str {
    match hash.len() {
        32  => "MD5",
        40  => "SHA-1",
        56  => "SHA-224",
        64  => "SHA-256",
        96  => "SHA-384",
        128 => "SHA-512",
        _   => "Unknown",
    }
}

fn cmd_hashid(hash: &str) {
    let kind = identify_hash(hash);
    println!("\n  {}Hash  :{} {}{}{}", Y, W, C, hash, RST);
    println!("  {}Type  :{} {}{}{}", Y, W, G, kind, RST);
    println!("  {}Length:{} {}{}{}\n", Y, W, G, hash.len(), RST);
}

// ── Password strength checker ──────────────────────────────
fn cmd_pwcheck(pw: &str) {
    let has_upper = pw.chars().any(|c| c.is_uppercase());
    let has_lower = pw.chars().any(|c| c.is_lowercase());
    let has_digit = pw.chars().any(|c| c.is_ascii_digit());
    let has_sym   = pw.chars().any(|c| !c.is_alphanumeric());
    let len       = pw.len();

    let mut score = 0u8;
    if len >= 8  { score += 1; }
    if len >= 12 { score += 1; }
    if len >= 16 { score += 1; }
    if has_upper { score += 1; }
    if has_lower { score += 1; }
    if has_digit { score += 1; }
    if has_sym   { score += 1; }

    let strength = match score {
        0..=2 => format!("{}WEAK{}",   R, RST),
        3..=4 => format!("{}MEDIUM{}", Y, RST),
        5..=6 => format!("{}STRONG{}", G, RST),
        _     => format!("{}VERY STRONG{}", C, RST),
    };

    println!("\n  {}Password  :{} {}{}{}",  Y, W, C, pw, RST);
    println!("  {}Length    :{} {}{}{}",    Y, W, G, len, RST);
    println!("  {}Uppercase :{} {}{}{}",    Y, W, G, has_upper, RST);
    println!("  {}Lowercase :{} {}{}{}",    Y, W, G, has_lower, RST);
    println!("  {}Digits    :{} {}{}{}",    Y, W, G, has_digit, RST);
    println!("  {}Symbols   :{} {}{}{}",    Y, W, G, has_sym,   RST);
    println!("  {}Strength  :{} {}\n",      Y, W, strength);
}

// ── Subdomain wordlist probe ───────────────────────────────
fn cmd_subdomain(domain: &str) {
    let wordlist = vec![
        "www", "mail", "ftp", "api", "dev", "staging", "admin",
        "blog", "shop", "app", "cdn", "static", "img", "vpn",
        "remote", "portal", "secure", "test", "beta", "old",
        "new", "login", "auth", "m", "mobile", "ns1", "ns2",
        "smtp", "pop", "imap", "webmail", "autodiscover",
    ];

    println!("\n{}{}[*]{} Probing subdomains of: {}{}{}\n", C, B, RST, Y, domain, RST);

    let mut found = 0;
    for sub in &wordlist {
        let fqdn = format!("{}.{}", sub, domain);
        // DNS-via-TCP-connect probe (port 80)
        let addr = format!("{}:80", fqdn);
        if TcpStream::connect_timeout(
            &addr.parse().unwrap_or_else(|_| "0.0.0.0:80".parse().unwrap()),
            Duration::from_millis(500),
        ).is_ok() {
            println!("  {}[FOUND]{} {}{}{}", G, W, C, fqdn, RST);
            found += 1;
        }
    }

    if found == 0 {
        println!("  {}[!] No subdomains responded from wordlist.{}", R, RST);
    } else {
        println!("\n  {}[+] {} subdomain(s) found.{}\n", G, found, RST);
    }
}

// ── Caesar cipher ─────────────────────────────────────────
fn cmd_caesar(text: &str, shift: i32) {
    let shifted: String = text.chars().map(|c| {
        if c.is_ascii_alphabetic() {
            let base = if c.is_uppercase() { b'A' } else { b'a' };
            let shifted = ((c as i32 - base as i32 + shift).rem_euclid(26)) as u8 + base;
            shifted as char
        } else { c }
    }).collect();
    println!("\n  {}Input :{} {}{}{}",  Y, W, C, text,    RST);
    println!("  {}Shift :{} {}{}{}",    Y, W, G, shift,   RST);
    println!("  {}Output:{} {}{}{}\n",  Y, W, G, shifted, RST);
}

// ── Base64 encode/decode ───────────────────────────────────
const B64: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

fn b64_encode(data: &[u8]) -> String {
    let mut out = String::new();
    for chunk in data.chunks(3) {
        let b0 = chunk[0] as usize;
        let b1 = if chunk.len() > 1 { chunk[1] as usize } else { 0 };
        let b2 = if chunk.len() > 2 { chunk[2] as usize } else { 0 };
        out.push(B64[b0 >> 2] as char);
        out.push(B64[((b0 & 3) << 4) | (b1 >> 4)] as char);
        out.push(if chunk.len() > 1 { B64[((b1 & 0xf) << 2) | (b2 >> 6)] as char } else { '=' });
        out.push(if chunk.len() > 2 { B64[b2 & 0x3f] as char } else { '=' });
    }
    out
}

fn cmd_b64(text: &str, decode: bool) {
    if !decode {
        let enc = b64_encode(text.as_bytes());
        println!("\n  {}Encoded:{} {}{}{}\n", Y, W, G, enc, RST);
    } else {
        println!("  {}[!] Base64 decode: use 'base64 -d' system tool for now.{}\n", Y, RST);
    }
}

// ── Main ──────────────────────────────────────────────────
fn main() {
    let args: Vec<String> = env::args().collect();
    banner();

    if args.len() < 2 {
        println!("{}Commands:{}", Y, RST);
        println!("  {}hashid   <hash>           {}Identify hash type", C, W);
        println!("  {}pwcheck  <password>       {}Check password strength", C, W);
        println!("  {}subdomain <domain>        {}Probe subdomains", C, W);
        println!("  {}caesar   <text> <shift>   {}Caesar cipher", C, W);
        println!("  {}b64      <text>            {}Base64 encode\n", C, W);
        return;
    }

    match args[1].as_str() {
        "hashid" => {
            if args.len() < 3 { eprintln!("{}Usage: sub-recon hashid <hash>{}", R, RST); }
            else { cmd_hashid(&args[2]); }
        }
        "pwcheck" => {
            if args.len() < 3 { eprintln!("{}Usage: sub-recon pwcheck <password>{}", R, RST); }
            else { cmd_pwcheck(&args[2]); }
        }
        "subdomain" => {
            if args.len() < 3 { eprintln!("{}Usage: sub-recon subdomain <domain>{}", R, RST); }
            else { cmd_subdomain(&args[2]); }
        }
        "caesar" => {
            if args.len() < 4 { eprintln!("{}Usage: sub-recon caesar <text> <shift>{}", R, RST); }
            else {
                let shift = args[3].parse::<i32>().unwrap_or(13);
                cmd_caesar(&args[2], shift);
            }
        }
        "b64" => {
            if args.len() < 3 { eprintln!("{}Usage: sub-recon b64 <text>{}", R, RST); }
            else { cmd_b64(&args[2], false); }
        }
        _ => eprintln!("{}[!] Unknown command: {}{}", R, args[1], RST),
    }
}
