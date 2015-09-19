CC = clang++
ARCH = -arch x86_64

OCVDIR = /home/cshome/s/steven/Public/OpenCV/

INCLUDE_FLAGS=-I$(OCVDIR)/include

CFLAGS = -c -std=c++11 -Wall -Wpedantic -Werror $(INCLUDE_FLAGS)
LDFLAGS = -L$(OCVDIR)/lib -lopencv_core -lopencv_highgui -lopencv_imgproc

SOURCES = ocvTest.cpp
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = ocvTest


all : $(SOURCES) $(EXECUTABLE)

clean :
	rm -rf $(OBJECTS) $(EXECUTABLE) *~ core

$(EXECUTABLE): $(OBJECTS) Makefile
	$(CC) $(ARCH) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@