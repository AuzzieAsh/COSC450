CC=g++
ARCH=-arch x86_64

OCVDIR=/home/cshome/s/steven/Public/OpenCV

INCLUDE_FLAGS=-I$(OCVDIR)/include

CFLAGS=-c -Wall $(INCLUDE_FLAGS)
LDFLAGS= -L$(OCVDIR)/lib -lopencv_core -lopencv_highgui -lopencv_imgproc

SOURCES=segmentation.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=segmentation


all : $(SOURCES) $(EXECUTABLE)

clean :
	rm -rf $(OBJECTS) $(EXECUTABLE) *~ core

$(EXECUTABLE): $(OBJECTS) Makefile
	$(CC) $(ARCH) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@