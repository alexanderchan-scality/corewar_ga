.name "gen_1_id_28"
.comment "gen_1_id_28"

	st		r1, 235
		and r1, %0, r1
live:	live %1
		zjmp %:live2
live2:
		zjmp %:live
	sti	r4, %:l2 - 100, r2
