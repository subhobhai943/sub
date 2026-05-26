; sysinfo.asm — x86-64 Linux Assembly: raw system info via syscalls
; Author : Subhobhai (subhobhai943)
; Assemble: nasm -f elf64 sysinfo.asm && ld -o sub-sysinfo sysinfo.o
;
; Prints: CPU architecture (uname syscall) and a hacker-style header.
; Extend with more syscalls as needed.

section .data
    banner_str  db  27,"[96m",27,"[1m", 10
                db  "  [SUB-SYSINFO] x86-64 Assembly Edition", 10
                db  27,"[0m", 0
    label_node  db  27,"[93m","  Node    : ",27,"[97m", 0
    label_kern  db  10,27,"[93m","  Kernel  : ",27,"[97m", 0
    label_arch  db  10,27,"[93m","  Machine : ",27,"[97m", 0
    newline     db  10,27,"[0m",10, 0
    err_str     db  27,"[91m","[!] uname syscall failed",27,"[0m",10, 0

section .bss
    ; uname struct layout (Linux x86-64): 6 fields x 65 bytes each = 390 bytes
    uname_buf   resb 390

section .text
    global _start

; Helper: print null-terminated string at rsi, length in rdx using write(1,...)
print_str:
    ; find length
    push    rsi
    xor     rcx, rcx
.len_loop:
    cmp     byte [rsi + rcx], 0
    je      .done_len
    inc     rcx
    jmp     .len_loop
.done_len:
    mov     rdx, rcx
    pop     rsi
    mov     rax, 1          ; sys_write
    mov     rdi, 1          ; stdout
    syscall
    ret

; Helper: print field from uname_buf at offset rsi (65-byte field)
print_uname_field:
    ; rsi = pointer to start of 65-byte field
    mov     rdx, 65
    mov     rax, 1
    mov     rdi, 1
    syscall
    ret

_start:
    ; --- Call uname(2) syscall (number 63 on x86-64) ---
    mov     rax, 63         ; sys_uname
    lea     rdi, [uname_buf]
    syscall
    cmp     rax, 0
    jne     .error

    ; --- Print banner ---
    lea     rsi, [banner_str]
    call    print_str

    ; --- Print Nodename (offset 65) ---
    lea     rsi, [label_node]
    call    print_str
    lea     rsi, [uname_buf + 65]   ; nodename
    call    print_uname_field

    ; --- Print Kernel release (offset 130) ---
    lea     rsi, [label_kern]
    call    print_str
    lea     rsi, [uname_buf + 130]  ; release
    call    print_uname_field

    ; --- Print Machine/arch (offset 260) ---
    lea     rsi, [label_arch]
    call    print_str
    lea     rsi, [uname_buf + 260]  ; machine
    call    print_uname_field

    ; --- Newline + reset ---
    lea     rsi, [newline]
    call    print_str

    ; --- exit(0) ---
    mov     rax, 60
    xor     rdi, rdi
    syscall

.error:
    lea     rsi, [err_str]
    call    print_str
    mov     rax, 60
    mov     rdi, 1
    syscall
