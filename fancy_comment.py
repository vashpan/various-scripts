#!/usr/bin/python3

# This 

import sys, string

COMMENT_LENGTH = 80

def print_error(msg):
    print('Error: ' + msg)
    exit(1)

if len(sys.argv) != 2:
    print_error('Usage: %s <text>' % sys.argv[0])

text = (' ' + sys.argv[1] + ' ').upper()
start = int((COMMENT_LENGTH - len(text)) / 2 ) 
end = int(COMMENT_LENGTH - start - len(text))

print('/' + '*' * COMMENT_LENGTH + '/')
print('/' + '*' * start + text + '*' * end + '/')
print('/' + '*' * COMMENT_LENGTH + '/')
