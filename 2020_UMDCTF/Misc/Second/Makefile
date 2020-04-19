CC=gcc
flags=-fpie -Wshadow -fno-stack-protector
source=second.c
out=second

all: second

second: second.c
	$(CC) $(source) -o $(out) $(flags)
