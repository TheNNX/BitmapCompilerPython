[bits 32]
[section .text]
[global _DllMain@12]
[global _NNXInit@0]
[global _NNXPrint]
[global _GetStack@0]
[global _Test@0]

[export _DllMain@12]
[export _NNXInit@0]
[export _NNXPrint@4]
[export _GetStack@0]
[export _Test@0]

[extern _DebugBreak@0]
[extern _WriteConsoleA@20]
[extern _GetStdHandle@4]
[extern _AllocConsole@0]



_DllMain@12:
	mov eax, 1
	ret 12
	
_NNXInit@0:
	push dword -11
	call _GetStdHandle@4
	
	push dword 0
	push dword written
	push dword 7
	push dword done1
	push dword eax
	call _WriteConsoleA@20
	
	ret 
	
_GetStack@0:
	mov eax, esp
	add eax, 4
	ret
	
_Test@0:
	push ebp
	mov ebp, esp
	
	push 0x61616161
	push byte 0x0
	call _NNXPrint
	
	pop ebp
	ret
	
; [EBP + 9] = char1
; [EBP + 8] = len
; [EBP + 4] = return
_NNXPrint:
	push ebp
	mov ebp, esp
	
	mov eax, esp
	add al, [ebp + 8]
	jnc .DontInc
	add eax, 0x100
.DontInc:
	add eax, 9
	push dword eax
	
	mov eax, [ebp + 4]
	push dword eax

.Loop:
	
	cmp byte [ebp + 8], 0
		jna .End
	
	mov al, [ebp + 9]
	mov [tempBuffer], al
	
	push dword -11
	call _GetStdHandle@4
	
	push dword 0
	push dword written
	push dword 1
	push dword tempBuffer
	push dword eax
	call _WriteConsoleA@20
	
	dec byte [ebp + 8]
	
	jmp .Loop
	
.End:	

	pop eax
	pop ebp
	pop esp
	xchg ebp, esp
	jmp eax
	
	
[section .data]
tempBuffer: db 'abc'
written: dd 0x00000000
returnAddress: dd 0x00000000
tempEbp: dd 0x00000000
counter: db 0x00
max: db 0x00
done1: db "NNXInit", 0