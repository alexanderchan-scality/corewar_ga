.name		"zorkyou"
.comment	"brain fuck <3"

prep_live:
	sti		r1, %:while_live_1, %1
	sti		r1, %:while_live_2, %1
	sti		r1, %:zork_you, %1
	sti		r1, %:do_live, %1

send_zork:
	st		r1, 6
	live	%255
	fork	%:zork_you

while_prep:
	ld		%16777216, r6
	ld		%1, r8
	ld		%5, r10
	ld		%4, r11

while_prep_1:
	ld		%0, r7
	ld		%-3, r9

while_start_1:
	add		r7, r8, r7

while_verif_1:
	xor		r7, %70, r16

while_live_1:
	live	%50

while_stop_1:
	zjmp	%:while_end_1

while_calc_pos_1:
	sub		r9, r10, r9
	add		r9, r11, r12

while_write_1:
	sti		r8, %:prep_live, r9

while_restart_1:
	ld		%0, r16
	zjmp	%:while_start_1

while_end_1:
	st		r1, 6
	live	%255
	fork	%:prep_live

while_prep_2:
	ld		%0, r7
	ld		%0, r9

while_start_2:
	add		r7, r8, r7

while_verif_2:
	xor		r7, %70, r16

while_live_2:
	live	%255

while_stop_2:
	zjmp	%:while_end_2

while_calc_pos_2:
	add		r9, r10, r9
	add		r9, r8, r12

while_write_2:
	sti		r6, %:zork_you, r9
	sti		r1, %:zork_you, r12

while_restart_2:
	ld		%0, r16
	zjmp	%:while_start_2

while_end_2:
	st		r1, 6
	live	%255
	fork	%:prep_live
	ld		%0, r16

do_live:
	live	%255
	zjmp	%:do_live

zork_you:
	live	%255
