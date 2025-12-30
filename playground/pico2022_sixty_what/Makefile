CC=gcc
CFLAGS= -fno-stack-protector -z execstack -no-pie -Wall -Wextra
LDFLAGS= -no-pie
TARGET=vuln
SRC=vuln.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean
