import sys

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
  return tuple(p)

# generate all branch of p
def posgen(p):
  pos.add(p)
  if (p[0]|p[1]|p[2] == 0) or (p[4]|p[5]|p[6] == 0):
    return
  o = p[8]<<2
  if p[o]:
    posgen(move(p,0))
  if p[o+1]:
    posgen(move(p,1))
  if p[o+2]:
    posgen(move(p,2))

def enc(p):
  return ''.join([chr(i+48) for i in p[:3]+p[4:7]+(p[8],)])

def minify(ps):
  return set(map(enc, ps))

pos = set()
posgen((3,3,3,0,3,3,3,0,0))
minified = minify(pos)
print('positions = ', end='')
print(minified)
print("%d positions generated" % len(minified), file=sys.stderr)