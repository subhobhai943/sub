; sub - The SUB Hacking & Info Tool (x86-64 Assembly / NASM)
; Author: Subhobhai (subhobhai943)
; GitHub: https://github.com/subhobhai943
; Assemble: nasm -f elf64 sub.asm -o sub.o && ld sub.o -o sub

section .data
    banner      db  10
                db  "  +-+-+-+", 10
                db  "  |S|U|B|", 10
                db  "  +-+-+-+", 10
                db  "  by Subhobhai | github.com/subhobhai943", 10
                db  "  x86-64 Assembly Edition", 10, 10
    banner_len  equ $ - banner

    msg_whoami  db  "  Name       : Subhobhai Sarkar", 10
                db  "  Alias      : sub", 10
                db  "  GitHub     : https://github.com/subhobhai943", 10
                db  "  Portfolio  : https://sub-portofolio.netlify.app", 10
                db  "  Location   : Durgapur, West Bengal, India", 10
                db  "  Arch       : x86-64", 10, 10
    whoami_len  equ $ - msg_whoami

    msg_usage   db  "Usage: sub [banner|whoami]", 10
                db  "  banner   - Show ASCII banner", 10
                db  "  whoami   - Author info", 10, 10
    usage_len   equ $ - msg_usage

    arg_banner  db  "banner", 0
    arg_whoami  db  "whoami", 0

section .text
    global _start

; sys_write(fd=1, buf, len)
%macro print 2
    mov rax, 1
    mov rdi, 1
    mov rsi, %1
    mov rdx, %2
    syscall
%endmacro

; strcmp: rsi=str1, rdi=str2 -> rax=0 if equal
strcmp:
    .loop:
        mov al, [rsi]
        mov bl, [rdi]
        cmp al, bl
        jne .not_equal
        test al, al
        jz  .equal
        inc rsi
        inc rdi
        jmp .loop
    .equal:
        xor rax, rax
        ret
    .not_equal:
        mov rax, 1
        ret

_start:
    pop rbx           ; argc
    cmp rbx, 1
    jle .show_usage

    pop rax           ; argv[0] skip
    pop rsi           ; argv[1] = command

    mov rdi, arg_banner
    call strcmp
    test rax, rax
    jz .do_banner

    pop rsi
    mov rdi, arg_whoami
    call strcmp
    test rax, rax
    jz .do_whoami

.show_usage:
    print msg_usage, usage_len
    jmp .exit

.do_banner:
    print banner, banner_len
    jmp .exit

.do_whoami:
    print banner, banner_len
    print msg_whoami, whoami_len

.exit:
    mov rax, 60
    xor rdi, rdi
    syscall
