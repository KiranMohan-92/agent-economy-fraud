# Makefile for arXiv paper compilation
# Usage: make (builds PDF), make clean (removes build artifacts)

MAIN = main
LATEX = pdflatex
BIBTEX = bibtex

.PHONY: all clean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex references.bib abstract.tex introduction.tex background.tex \
             threat_model.tex detection_framework.tex evaluation.tex related_work.tex \
             recommendations.tex limitations.tex conclusions.tex \
             appendix_signals.tex appendix_dataset.tex appendix_reproducibility.tex
	$(LATEX) -interaction=nonstopmode $(MAIN)
	$(BIBTEX) $(MAIN)
	$(LATEX) -interaction=nonstopmode $(MAIN)
	$(LATEX) -interaction=nonstopmode $(MAIN)

clean:
	rm -f $(MAIN).pdf $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log \
	      $(MAIN).out $(MAIN).toc $(MAIN).lof $(MAIN).lot $(MAIN).fls \
	      $(MAIN).fdb_latexmk *.aux
