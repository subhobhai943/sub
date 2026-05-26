/**
 * sub - The SUB Hacking & Info Tool (Haxe)
 * Author: Subhobhai (subhobhai943)
 * GitHub: https://github.com/subhobhai943
 *
 * Haxe compiles to: JS, Python, C++, Java, C#, PHP, Lua, and more.
 * Build targets below.
 */

class Sub {

    static final BANNER =
        '\n' +
        '  +-+-+-+\n' +
        '  |S|U|B|\n' +
        '  +-+-+-+\n' +
        '  by Subhobhai | github.com/subhobhai943\n' +
        '  Haxe Edition\n';

    static final INFO:Array<Array<String>> = [
        ["Name",      "Subhobhai Sarkar"],
        ["Alias",     "sub"],
        ["GitHub",    "https://github.com/subhobhai943"],
        ["Portfolio", "https://sub-portofolio.netlify.app"],
        ["Location",  "Durgapur, West Bengal, India"],
        ["Bio",       "PCMB student | Web, AI, C++/C# game dev | Open-source hacker"],
        ["Projects",  "AIOS, SUB lang, Discord bots, 3D web games"],
        ["Languages", "Python, C, C++, Rust, Kotlin, Java, JS, Haxe, CUDA, Assembly"],
    ];

    static function banner():Void {
        Sys.println(BANNER);
    }

    static function whoami():Void {
        Sys.println(BANNER);
        for (row in INFO) {
            var key = row[0];
            var val = row[1];
            // Pad key to 12 chars
            while (key.length < 12) key += ' ';
            Sys.println('  ' + key + ': ' + val);
        }
        Sys.println('');
    }

    static function sysInfo():Void {
        Sys.println('\n[*] System Information');
        Sys.println('  OS      : ' + Sys.systemName());
        Sys.println('  Haxe    : ' + #if (haxe_ver >= 4) "4.x+" #else "3.x" #end);
        Sys.println('  Target  : ' + getTarget());
        Sys.println('');
    }

    static function getTarget():String {
        #if js      return "JavaScript";  #end
        #if python  return "Python";      #end
        #if cpp     return "C++";         #end
        #if java    return "Java";        #end
        #if cs      return "C#";          #end
        #if php     return "PHP";         #end
        #if lua     return "Lua";         #end
        #if neko    return "Neko VM";     #end
        #if hl      return "HashLink";    #end
        return "Unknown";
    }

    static function printHelp():Void {
        Sys.println(BANNER);
        Sys.println('Usage: sub <command>\n');
        Sys.println('Commands:');
        Sys.println('  banner   Show ASCII banner');
        Sys.println('  whoami   Author info');
        Sys.println('  info     System information');
        Sys.println('');
        Sys.println('GitHub: https://github.com/subhobhai943');
        Sys.println('');
    }

    static function main():Void {
        final args = Sys.args();
        if (args.length == 0) { printHelp(); return; }
        switch (args[0]) {
            case "banner": banner();
            case "whoami": whoami();
            case "info":   sysInfo();
            default:       printHelp();
        }
    }
}
