import tkinter
import math

MAPX = 8
MAPY = 8
MAPS = 64

Map = [
  1, 1, 1, 1, 1, 1, 1, 1,
  1, 0, 1, 0, 0, 0, 0, 1,
  1, 0, 1, 0, 0, 0, 0, 1,
  1, 0, 1, 0, 0, 0, 0, 1,
  1, 0, 0, 0, 0, 0, 0, 1,
  1, 0, 0, 0, 0, 1, 0, 1,
  1, 0, 0, 0, 0, 0, 0, 1,
  1, 1, 1, 1, 1, 1, 1, 1
]

win = tkinter.Tk()
win.resizable(False, False)
can = tkinter.Canvas(win, width=1024, height=510)

px = py = 300.0
pa = math.pi
pdx = 5.0* math.cos(pa)
pdy = 5.0* math.sin(pa)

PI2 = math.pi/2.0
PI3 = 3.0*math.pi/2.0

DR = 0.0174533

def fix_ang(num):
  if(num > 2*math.pi): return num-2*math.pi
  if(num < 0): return num+2*math.pi
  return num

def dist(ax,ay,bx,by):
  return math.sqrt((bx-ax)*(bx-ax) + (by-ay)*(by-ay))

def draw_rays():
  global pa, py, px, Map
  mx = my = mp = dof = 0
  rx = ry = ra = x0 = y0 = 0.0
  distT=1.0
  ra = fix_ang(pa+30.0*DR)
  for r in range(60):
    # Horizontal lines
    dof = 0
    distH=100000
    hx=px
    hy=py
    atan = -1.0 / math.tan(ra)
    color=None
    if(ra>math.pi): # looking up
      ry = ((int(py) >> 6) << 6)-0.0001
      rx = (py-ry)*atan+px
      y0 = -64
      x0 = -y0*atan
    elif (ra<math.pi): # looking down
      ry = ((int(py) >> 6) << 6) + 64
      rx = (py-ry)*atan+px
      y0 = 64
      x0 = -y0*atan
    elif ra == 0 or ra == math.pi: # looking straight left or right
      rx = px
      ry = py
      dof = 8

    while dof < 8:
      mx = int(rx) >> 6
      my = int(ry) >> 6
      mp = my * MAPX + mx
      if mp > 0 and mp < MAPX*MAPY and Map[mp] == 1: # hit the wall
        hx=rx
        hy=ry
        distH=dist(px,py,hx,hy)
        dof = 8
      else: # next line
        rx += x0
        ry += y0
        dof += 1

    # Vertical lines
    dof = 0
    distV=100000
    vx=px
    vy=py
    ntan = -math.tan(ra)
    if(ra>PI2 and ra <PI3): # looking up
      rx = ((int(px) >> 6) << 6)-0.0001
      ry = (px-rx)*ntan+py
      x0 = -64
      y0 = -x0*ntan
    elif (ra<PI2 or ra>PI3): # looking down
      rx = ((int(px) >> 6) << 6) + 64
      ry = (px-rx)*ntan+py
      x0 = 64
      y0 = -x0*ntan
    elif ra == 0 or ra == math.pi: # looking straight left or right
      rx = px
      ry = py
      dof = 8

    while dof < 8:
      mx = int(rx) >> 6
      my = int(ry) >> 6
      mp = my * MAPX + mx
      if mp > 0 and mp < MAPX*MAPY and Map[mp] == 1: # hit the wall
        vx=rx
        vy=ry
        distV=dist(px,py,vx,vy)
        dof = 8
      else: # next line
        rx += x0
        ry += y0
        dof += 1

    if distV<distH:
      rx=vx
      ry=vy
      distT=distV
      color='#ff0000'
    else:
      rx=hx
      ry=hy
      distT=distH
      color='#aa0000'
    can.create_line(px+4, py+4, rx,ry, fill='#00ff00')

    ca = fix_ang(pa-ra)
    distT=distT*math.cos(ca)
    lineH=MAPS*400/distT
    if lineH > 400: lineH = 400
    lineO = 200 - lineH/2
    can.create_line(r*8+530,lineO,r*8+530,lineH+lineO,fill=color,width=10)
    ra=fix_ang(ra-DR)

def draw_player():
  can.create_rectangle(px,py,px+8,py+8,fill='#ff0000')
  can.create_line(px+4,py+4,px+pdx*5,py+pdy*5,fill='#00ff00')

def draw_world():
  global Map
  for y in range(8):
    for x in range(8):
      color = '#000000'
      if Map[y*MAPX + x] == 1: color = '#ffffff'
      x0 = MAPS*x
      y0 = MAPS*y
      can.create_rectangle(x0+1, y0+1, x0+MAPS-1, y0+MAPS-1, fill=color)

def keyboard(event):
  global px, py, pa, pdx, pdy
  if event.keysym == 'w':
    px += pdx
    py += pdy
  elif event.keysym == 's':
    px -= pdx
    py -= pdy
  elif event.keysym == 'd':
    pa -= 0.1
    if pa < 0: pa += 2.0 * math.pi
    pdx = 5.0* math.cos(pa)
    pdy = 5.0* math.sin(pa)
  elif event.keysym == 'a':
    pa += 0.1
    if pa > 2.0 * math.pi: pa -= 2.0 * math.pi
    pdx = 5.0* math.cos(pa)
    pdy = 5.0* math.sin(pa)


  can.delete('all')
  draw_world()
  draw_player()
  draw_rays()


if __name__ == "__main__":
  win.bind("<Key>", keyboard)
  draw_world()
  draw_player()
  draw_rays()
  can.pack()
  win.mainloop()
