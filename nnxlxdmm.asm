[bits 32]
[section .text]
[global _DllMain]
[global _NNXInit]
[global _NNXPrint]

[extern _DebugBreak@0]
[extern _WriteConsoleA@20]
[extern _GetStdHandle@4]
[export _DllMain]
[export _NNXInit]
[export _NNXPrint]
[extern _AllocConsole@0]


_DllMain:
	mov eax, 1
	ret 12
	
_NNXInit:
	push dword -11
	call _GetStdHandle@4
	
	push dword 0
	push dword written
	push dword 7
	push dword done1
	push dword eax
	call _WriteConsoleA@20
	
	ret 
	
; [BP + 9] = char1
; [BP + 8] = len
; [BP + 4] = return
_NNXPrint:
	jmp $
	mov eax, [esp]
	
	mov [returnAddress], eax
	mov [tempEbp], ebp
	
	mov ebp, esp

.Loop:	
	mov al, [bp + 9]
	mov [tempBuffer], al
	
	push dword -11
	call _GetStdHandle@4
	
	push dword 0
	push dword written
	push dword 1
	push dword tempBuffer
	push dword eax
	call _WriteConsoleA@20
	
	mov al, [tempBuffer]
	test al, al
		jz .End
	
	mov al, [counter]
	cmp al, [max]
		jge .End
	
	inc al
	mov [counter], al
	
	jmp .Loop
	
.End:
	jmp $
	and eax, 0xFF
	add esp, eax
	mov ebp, [tempEbp]
	mov eax, [returnAddress]
	push eax
	ret
	
[section .data]
tempBuffer: dw 0x0000
written: dd 0x00000000
returnAddress: dd 0x00000000
tempEbp: dd 0x00000000
counter: db 0x00
max: db 0x00
done1: db "NNXInit", 0