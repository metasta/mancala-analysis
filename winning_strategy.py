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

# generates strategical branch (1st player always makes best move)
def strategical_posgen(p):
  if (db[p][1] < 2):
    return
  if (p[8] == 0):
    next_pos = [move(p,i) for i in range(3) if p[i]]
    winning_next = list(filter(lambda x: db[x][0] == 0, next_pos))
    min_win = min([db[x][1] for x in winning_next])
    best = list(filter(lambda x: db[x][1] == min_win, winning_next))[0]
    if len(next_pos) > 1:
      spos[p] = [db[x] for x in next_pos]
    strategical_posgen(best)
  else:
    if p[4]:
      strategical_posgen(move(p,0))
    if p[5]:
      strategical_posgen(move(p,1))
    if p[6]:
      strategical_posgen(move(p,2))

def enc(p):
  return "".join([chr(i+48) for i in p[:3]+p[4:7]+(p[8],)])

def minify(s):
  return dict([(enc(k),v) for k,v in s.items()])

spos = dict()
strategical_posgen((3,3,3,0,3,3,3,0,0))
print("%d positions for winning" % len(spos))
print(minify(spos))
