import sys
import db
mdb = db.db

def dec(p):
  l = [ord(c)-48 for c in p]
  return tuple(l[:3] + [0] + l[3:6] + [0] + [l[6]])

def move(position, i):
  p = list(position)
  o = p[8]<<2
  j = i+o
  c = d = p[j]
  p[j] = 0
  while c > 0:
    p[(j+c)&7] += 1
    c -= 1
  if (p[o]|p[o+1]|p[o+2] == 0) or ((j+d+1)&3):
    p[8] = 1 - p[8]
  p[3] = p[7] = 0
  return tuple(p)

db = dict([ (dec(k),(v&1,v>>1)) for k,v in mdb.items()])

# find a route from initial position to p
def route(p):
  stack = [p]
  c = p
  while stack[0] != (3,3,3,0,3,3,3,0,0):
    for s in db:
      found = 0
      next_pos = [move(s,i) for i in range(3) if s[i+(s[8]<<2)]]
      if c in next_pos:
        found = 1
        stack.insert(0,s)
        c = s
        break
    if not found:
       print("error: not found", file=sys.stderr)
       return stack
  return stack

def enc(p):
  return "".join([chr(i+48) for i in p[:3]+p[4:7]+(p[8],)])

print(list(map(enc, route(dec(sys.argv[1])))))
