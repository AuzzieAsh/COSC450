FILE=Report

default: pdf

pdf:
	pdflatex $(FILE)

count:
	detex $(FILE).tex | wc -w

clean:
	rm -f *.aux
	rm -f *.bbl
	rm -f *.blg
	rm -f *.glg
	rm -f *.glo
	rm -f *.gls
	rm -f *.ist
	rm -f *.log
	rm -f *.out
	rm -f *.toc
	rm -f *~
	rm -f .DS_Store
