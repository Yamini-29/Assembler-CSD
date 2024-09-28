    MOV R0, #13       ; Load immediate value 13 into R0 (message length)
    #loading
    LDR R1, =hello    ; Load the address of the message into R1
    MOV R2, R0        ; Copy length to R2 (second argument)
    MOV R7, #4        ; Syscall number for sys_write in R7
    # moving

    MOV R7, #1        ; Syscall number for sys_exit
    MOV R0, #0        ; Exit code 0
    SVC 0             ; Call kernel
