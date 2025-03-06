sections := abstract-and-keywords.latex introduction.latex
sections += function-description.latex data-description.latex
sections += software-interface-description.latex
sections += software-behavior-description.latex
sections += restrictions-and-limitations.latex appendices.latex
sections += conclusion.latex acknowledgment.latex bibliography.latex
sections := $(sections:%=sections/%)

images := images/architecture-diagram.png
images += images/speech-response-loop.png
images += images/user-diagram.png

rep_name := Team_1_Progress_Report_1

$(rep_name).pdf: $(rep_name).latex IEEEtran.cls $(sections) $(images)
	pdflatex $(rep_name).latex
	pdflatex $(rep_name).latex
