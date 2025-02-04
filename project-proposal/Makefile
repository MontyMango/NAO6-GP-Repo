sections := abstract-and-keywords.latex background-and-objective.latex
sections += bibliography.latex development-team.latex introduction.latex
sections += key-technologies.latex project-schedule.latex
sections += system-and-functionality.latex
sections := $(sections:%=sections/%)

prop_name := Team_1_proposal

$(prop_name).pdf: $(prop_name).latex IEEEtran.cls $(sections)
	pdflatex $(prop_name).latex
