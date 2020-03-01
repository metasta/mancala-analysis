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

won_1st = 0
won_2nd = 0
winning_1st = 0
winning_2nd = 0
fork_1st = 0
fork_2nd = 0
misleading_fork_1st = {}
misleading_fork_2nd = {}
for k,v in db.items():
  if v[1] == 0:
    if v[0] == 0:
      won_1st += 1
      continue
    if v[0] == 1:
      won_2nd += 1
      continue
  if v[0] == 0:
    winning_1st += 1
  else:
    winning_2nd += 1
  next_pos = [ move(k,i) for i in range(3) if k[(k[8]<<2)+i] ]
  result = [db[p][0] for p in next_pos]
  if (0 in result and 1 in result):
    if k[8] == 0:
      fork_1st += 1
    else:
      fork_2nd += 1
    turn = [(p[8], db[p][0]) for p in next_pos]
    if ((k[8],1-k[8]) in turn and (k[8],k[8]) not in turn):
      if k[8] == 0:
        misleading_fork_1st[k] = v
      else:
        misleading_fork_2nd[k] = v

def enc(p):
  return "".join([chr(i+48) for i in p[:3]+p[4:7]+(p[8],)])

def minify(s):
  return dict([(enc(k),v) for k,v in s.items()])

print("misleading-fork:")
print(minify(misleading_fork_1st))
print(minify(misleading_fork_2nd))

print("total positions: %d" % len(db))
print("finished: %d (1st: %d 2nd: %d)" % (won_1st + won_2nd, won_1st, won_2nd) )
print("unfinished: %d (1st: %d 2nd: %d)" % (winning_1st + winning_2nd, winning_1st, winning_2nd) )
print("fork (both winning- and losing-move exists):")
print("%d (1st: %d 2nd: %d)" % (fork_1st + fork_2nd, fork_1st, fork_2nd))
print("misleading-fork (winning but chain-moves are losing):")
print("%d (1st: %d 2nd: %d)" % (len(misleading_fork_1st) + len(misleading_fork_2nd), len(misleading_fork_1st), len(misleading_fork_2nd)))
