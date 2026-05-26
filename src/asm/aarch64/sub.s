// sub - The SUB Hacking & Info Tool (AArch64 Assembly / GAS)
// Author: Subhobhai (subhobhai943)
// GitHub: https://github.com/subhobhai943
// Assemble: as sub.s -o sub.o && ld sub.o -o sub
// Target: Linux AArch64 (Raspberry Pi, ARM servers, Termux, Apple M-series Linux VM)

.section .data

banner:
    .ascii "\n"
    .ascii "  +-+-+-+\n"
    .ascii "  |S|U|B|\n"
    .ascii "  +-+-+-+\n"
    .ascii "  by Subhobhai | github.com/subhobhai943\n"
    .ascii "  AArch64 Assembly Edition\n\n"
banner_end:

msg_whoami:
    .ascii "  Name       : Subhobhai Sarkar\n"
    .ascii "  Alias      : sub\n"
    .ascii "  GitHub     : https://github.com/subhobhai943\n"
    .ascii "  Portfolio  : https://sub-portofolio.netlify.app\n"
    .ascii "  Location   : Durgapur, West Bengal, India\n"
    .ascii "  Arch       : AArch64 (ARM64)\n\n"
msg_whoami_end:

msg_usage:
    .ascii "Usage: sub [banner|whoami]\n"
    .ascii "  banner   - Show ASCII banner\n"
    .ascii "  whoami   - Author info\n\n"
msg_usage_end:

str_banner: .asciz "banner"
str_whoami: .asciz "whoami"

.section .text
.global _start

// strcmp: x0=str1, x1=str2 -> x0=0 if equal
strcmp:
1:  ldrb    w2, [x0], #1
    ldrb    w3, [x1], #1
    cmp     w2, w3
    b.ne    2f
    cbz     w2, 3f
    b       1b
2:  mov     x0, #1
    ret
3:  mov     x0, #0
    ret

_start:
    ldr     x19, [sp]           // argc
    cmp     x19, #1
    b.le    show_usage

    ldr     x20, [sp, #16]      // argv[1]

    // check "banner"
    mov     x0, x20
    adr     x1, str_banner
    bl      strcmp
    cbz     x0, do_banner

    // check "whoami"
    mov     x0, x20
    adr     x1, str_whoami
    bl      strcmp
    cbz     x0, do_whoami

show_usage:
    adr     x1, msg_usage
    adr     x2, msg_usage_end
    sub     x2, x2, x1
    mov     x0, #1
    mov     x8, #64
    svc     #0
    b       do_exit

do_banner:
    adr     x1, banner
    adr     x2, banner_end
    sub     x2, x2, x1
    mov     x0, #1
    mov     x8, #64
    svc     #0
    b       do_exit

do_whoami:
    adr     x1, banner
    adr     x2, banner_end
    sub     x2, x2, x1
    mov     x0, #1
    mov     x8, #64
    svc     #0
    adr     x1, msg_whoami
    adr     x2, msg_whoami_end
    sub     x2, x2, x1
    mov     x0, #1
    mov     x8, #64
    svc     #0

do_exit:
    mov     x0, #0
    mov     x8, #93
    svc     #0
