[bits 32]
[section .text]
[global _DllMain@12]
[global _NNXInit@0]
[global _NNXPrint]
[global _GetStack@0]
[global _Test@0]
[global _NNXConditional@12]

[export _DllMain@12]
[export _NNXInit@0]
[export _NNXPrint]
[export _GetStack@0]
[export _Test@0]
[export _NNXConditional@12]

[extern _DebugBreak@0]
[extern _WriteConsoleA@20]
[extern _GetStdHandle@4]
[extern _AllocConsole@0]


_DllMain@12:
	mov eax, 1
	ret 12

;[EBP+16] - b
;[EBP+12] - a
;[EBP+8] - mode
_NNXConditional@12:
	push ebp
	mov ebp, esp
	pusha
	
	mov eax, [ebp+8]
	mov ebx, [ebp+16]
	mov ecx, [ebp+12]
	cmp eax, 0
		je .IsZero
	cmp eax, 1
		je .IsGreater
	cmp eax, 2
		je .IsNotGreater
	cmp eax, 3
		je .IsLess
	cmp eax, 4
		je .IsNotLess
	cmp eax, 5
		je .IsNotZero
		
.IsNotZero:
	xchg ecx, ebx
.IsZero:
	cmp ebx, ecx
		jz .True
	jmp .False
.IsNotGreater:
	xchg ebx, ecx
.IsGreater:
	cmp ebx, ecx
		jg .True
	jmp .False
.IsNotLess:
	xchg ebx, ecx
.IsLess:
	cmp ebx, ecx
		jl .True
	jmp .False
.False:
	xor eax, eax
	popa
	pop ebp
	ret
.True:
	mov eax, 1
	popa
	pop ebp
	ret
	
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
	
; [EBP + 12] = char1
; [EBP + 8] = len
; [EBP + 4] = return
; [EBP - 12] = current position
_NNXPrint:
	push ebp
	mov ebp, esp
	
	mov eax, [ebp + 8]
	shl eax, 2
	add eax, esp
	push dword eax
	
	mov eax, [ebp + 4]
	push dword eax

	mov eax, [ebp + 8]
	shl eax, 2
	add eax, ebp
	add eax, 8
	push dword eax
.Loop:
	
	cmp dword [ebp + 8], 0
		jna .End
	
	mov eax, [ebp - 12]
	
	mov al, [eax]
	mov [tempBuffer], al
	
	sub dword [ebp - 12], 4
	
	push dword -11
	call _GetStdHandle@4
	
	push dword 0
	push dword written
	push dword 1
	push dword tempBuffer
	push dword eax
	call _WriteConsoleA@20
	
	dec dword [ebp + 8]
	
	jmp .Loop
	
.End:	

	add esp, 4

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