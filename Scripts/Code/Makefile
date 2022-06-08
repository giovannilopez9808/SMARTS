CC=gfortran
SOURCES=smarts.f
CDFLAGS=-O3 -g
OBJECTS=$(SOURCES:.f=.out)


$(OBJECTS): $(SOURCES)
	$(CC) $(CDFLAGS) -o $(OBJECTS) $(SOURCES)
	mv $(OBJECTS) ../

clean:
	rm -f $(OBJECTS)
