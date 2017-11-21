// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
(START) 
	@24576
	D=M
	@BLANK 
	D;JEQ
	@0 
	D=A
	@i 
	M=D
	@8192
	D=A 
	@LIM_ONE
	M=D
(LOOP_ONE) 
	@LIM_ONE
	D=M
	@i 
	D=D-M
	@START
	D;JGT
	@i 
	D=A
	@SCREEN
	A=A+D 
	M=-1
	M=M+1
	@LOOP_ONE
	0;JMP
(BLANK)
	@0 
	D=A
	@i 
	M=D
	@8192
	D=A 
	@LIM_TWO
	M=D
(LOOP_TWO) 
	@LIM_TWO
	D=M
	@i 
	D=D-M
	@START
	D;JGT
	@i
	D=A
	@SCREEN
	A=A+D 
	M=0
	M=M+1
	@LOOP_TWO
	0;JMP