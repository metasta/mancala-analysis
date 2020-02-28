import sys
import PositionTable
enc_pos = PositionTable.positions

def dec(p):
  l = [ord(c)-48 for c in p]
  return tuple(l[:3] + [0] + l[3:6] + [0] + [l[6]])

pos = set(map(dec, enc_pos))

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

def solve(p):
  if p[0]|p[1]|p[2] == 0:
    solved[p] = [0,0]
    return
  if p[4]|p[5]|p[6] == 0:
    solved[p] = [1,0]
    return
  next_pos = [ move(p,i) for i in range(3) if p[(p[8]<<2)+i] ]
  known_next = list(filter(lambda x: x in solved, next_pos))
  winning_next = list(filter(lambda x: solved[x][0] == p[8], known_next))
  if winning_next:
    # one or more winning branch exists
    mv2win = min(map(lambda x: solved[x][1], winning_next)) + 1
    solved[p] = [p[8], mv2win]
    return
  if (len(next_pos) == len(known_next)) and not winning_next:
    # all branches are known to be losing
    mv2lose = max(map(lambda x: solved[x][1], next_pos)) + 1
    solved[p] = [1 - p[8], mv2lose]
    return

def analysis():
  prev_size = -1
  size = len(solved)
  print("solved positions: ", file=sys.stderr)
  while size != prev_size:
    prev_size = size
    for p in pos:
      solve(p)
    size = len(solved)
    print(size, file=sys.stderr)

def enc(p):
  return "".join([chr(i+48) for i in p[:3]+p[4:7]+(p[8],)])

def minify(s):
  return dict([ (enc(k),(v[1]<<1)+v[0]) for k,v in s.items()])
  
solved = {}
analysis()
print(minify(solved))