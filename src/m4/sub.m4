divert(-1)
dnl sub - The SUB Hacking & Info Tool (M4 Macro Language)
dnl Author: Subhobhai (subhobhai943)
dnl GitHub: https://github.com/subhobhai943
dnl Run: m4 sub.m4

define(`AUTHOR',    `Subhobhai Sarkar')dnl
define(`ALIAS',     `sub')dnl
define(`GITHUB',    `https://github.com/subhobhai943')dnl
define(`PORTFOLIO', `https://sub-portofolio.netlify.app')dnl
define(`LOCATION',  `Durgapur, West Bengal, India')dnl
define(`BIO',       `PCMB student | Web, AI, C++/C# game dev | Open-source hacker')dnl
define(`PROJECTS',  `AIOS, SUB lang, Discord bots, 3D web games')dnl
define(`LANGS',     `Python, C, C++, Rust, Kotlin, Java, JS, Assembly, M4, CUDA')dnl
define(`VERSION',   `1.0.0')dnl

define(`BANNER', `
  +-+-+-+
  |S|U|B|
  +-+-+-+
  by AUTHOR | GITHUB
  M4 Macro Edition v`'VERSION
')dnl

define(`WHOAMI_INFO', `BANNER
  Name       : AUTHOR
  Alias      : ALIAS
  GitHub     : GITHUB
  Portfolio  : PORTFOLIO
  Location   : LOCATION
  Bio        : BIO
  Projects   : PROJECTS
  Languages  : LANGS
')dnl

define(`USAGE_INFO', `
Usage: m4 sub.m4
  Edit the divert(0) section to control output.
  Macros: BANNER, WHOAMI_INFO
')dnl

divert(0)dnl
WHOAMI_INFO
