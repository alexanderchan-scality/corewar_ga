.name "Donald Motherfucking Trump"
.comment "Pushing chili eaters to their limits since 1946. Inventor of
new TV-reality political program named <<Build a wall in three lessons>>.
Future winner of extreme makeover in fence category. Proud owner of the
first hair yorkshire in the world. Absolute fan of
<<papers please>> !!! xoxo
PS : gonna make America great again suckers"

fuckukratos:
	zjmp		%-511

	ld			%851920, r4
	ld			%167936, r3
	st			r3, -25
	st			r4, -26
	ld			%984040, r2
	ld			%0, r16
	sti			r1, %:hairytaunt, %1
	fork		%:hairytaunt
	zjmp		%:antibeaneatersrush

buymaterials:
	live		%666
	ld			%1234567, r6
	ld			%0, r8
	st			r1, 31
	st			r1, 61
	st			r1, 91
	st			r1, 121
	st			r1, 151
	st			r1, 181

# Making Valery Damidot great again
ultimatewallbuilder:
	live		%3055151
	st			r2, -410
	st			r2, -407
	st			r2, -404
	st			r2, -401
	st			r2, -398
	st			r2, -395

	live		%9868977
	st			r2, -397
	st			r2, -394
	st			r2, -391
	st			r2, -388
	st			r2, -385
	st			r2, -382

	live		%3055151
	st			r2, -384
	st			r2, -381
	st			r2, -378
	st			r2, -375
	st			r2, -372
	st			r2, -369

	live		%9868977
	st			r2, -371
	st			r2, -368
	st			r2, -365
	st			r2, -362
	st			r2, -359
	st			r2, -356

	live		%9868977
	st			r2, -358
	st			r2, -355
	st			r2, -352
	st			r2, -349
	st			r2, -346
	st			r2, -343

	live		%9868977
	st			r2, -345
	st			r2, -342
	st			r2, -339
	st			r2, -336
	st			r2, -333
	st			r2, -330

	zjmp		%:ultimatewallbuilder

interncontract:
	st			r1, 38
	st			r1, 38
	st			r1, 38
	st			r1, 38
	st			r1, 38
	st			r1, 38

nationalisation:
	ld			%1, r16

sebastianomartineztheintern:
	live		%76544674
	live		%76544674
	live		%76544674
	live		%76544674
	live		%76544674
	live		%76544674
	zjmp		%:sebastianomartineztheintern
	fork		%:sebastianomartineztheintern
	ld			%0, r16
	zjmp		%:sebastianomartineztheintern

# First barrier against RAINBOW DASH THE MIGHTY MEXICANO
antibeaneatersrush:
	sti			r1, %:politicalcampaign, %1
	sti			r1, %:politicalcampaign, %9
	sti			r1, %:politicalcampaign, %17
	sti			r1, %:politicalcampaign, %25
	sti			r1, %:politicalcampaign, %33
	sti			r1, %:politicalcampaign, %41
	sti			r1, %:politicalcampaign, %49
	sti			r1, %:buymaterials, %1
	st			r1, 6
	live		%875765
	fork		%:buymaterials

# Recruiting slav*kof kof* hm i mean electors
politicalcampaign:
	live		%76578685
	fork		%:politicalcampaign
	live		%76578685
	fork		%:ultimatewallbuilder
	live		%76578685
	fork		%:buymaterials
	live		%65435454
	fork		%:buymaterials
	live		%65435454
	fork		%:interncontract
	live		%76578685
	fork		%:nationalisation
	live		%76578685
	fork		%:politicalcampaign
	zjmp		%:politicalcampaign

# L'oreal intrusion
hairytaunt:
	live		%666
	zjmp		%511
