section .data
    hello db 'Hello, World!', 0

section .text
    global _start

_start:
    mov edx, 13           ; Message length
    mov ecx, hello        ; Message to write
    mov ebx, 1            ; File descriptor (stdout)
    mov eax, 4            ; System call number (sys_write)
    int 0x80              ; Call kernel

    mov eax, 1            ; System call number (sys_exit)
    xor ebx, ebx          ; Exit code 0
    int 0x80              ; Call kernel
