// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
	@i 
	M=1 
	@MULT 
	M=0 
	@0 
	D=M
	@RZERO 
	M=D
	@1 
	D=M 
	@RONE 
	M=D 
	@2 
	M=0
	@RZERO 
	D=M
	@END
	D;JEQ
	@RONE 
	D=M
	@END
	D;JEQ
(LOOP)
	@i 
	D=M 
	@RONE
	D=D-M 
	@SAVE
	D;JGT 
	@RZERO
	D=M 
	@MULT
	M=D+M 
	@i 
	D=M 
	@i 
	D=M
	M=M+1
	@LOOP
	0;JMP
(SAVE) 
	@MULT
	D=M
	@2
	M=D 
	@END 
	0;JMP 
(END) 
	@END 
	0;JMP
	
	 
