// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
	@i 
	M=0 
	@MULT
	M=0 
	@0 
	D=M 
	@R_ZERO
	M=D 
	@1 
	D=M 
	@R_ONE
	M=D
(LOOP)
	@R_ZERO
	D=M
	@i 
	D=M
	@R_ONE
	D=D-M
	@LOOP
	D;JGT
		
(END)
	@END
	0;JMP