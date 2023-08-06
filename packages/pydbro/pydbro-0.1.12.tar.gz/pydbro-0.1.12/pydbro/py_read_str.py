#
# PROGRAM: PYTHON CONSOLE DATABASE BROWSER
# MODULE : READ USER INPUT AS STRING
#

import curses

def read_str(screen, col, p_banner, strdef = "", passwd = 0):

  curses.curs_set(1)
  curses.noecho()
  ch = 0
  prev_ch = 0
  if strdef != "":
    vstr = strdef
  else:
    vstr = ""
  screen.move(0,0)
  screen.addstr(p_banner,col["miGr"])
  #screen.move(1,0)
  #screen.addstr("-"*(wi-1),col["loGr"])
  screen.move(1,0)
  curx = 0
  cury = 0
  curword = 0
  if len(vstr)>0:
    if passwd == 1:
      screen.addstr("*"*(len(vstr)),col["hiGr"])
    else:
      screen.addstr(vstr,col["hiGr"])
  while ch != 10:
    #screen.clrtoeol()
    ch = screen.getch()
    sy, sx = screen.getyx()
    screen.move(2,0)
    #screen.addstr(str(ch)+"|"+str(prev_ch)+"|"+str(curx)+"|"+str(cury))
    screen.move(sy,sx)
    if (
         (ch >= ord(" ") and ch <= ord("~"))
      or (ch == 127 or ch == 263 or ch == 8 or ch == 91)
    ):
      strlen = len(vstr)
      screen.move(1,strlen)
      cury, curx = screen.getyx()
      #if ch == 91:
      #  ch = screen.getch()
      #  if ch == 68:
      #    if strlen > 1:
      #      newpos=0
      #      vstrarr = vstr.split(" ")
      #      if curword == 0:
      #        curword = len(vstrarr)
      #      if curword > 1:
      #        for i in vstrarr[:curword]:
      #          newpos += len(i)+1
      #        newpos=newpos-curword
      #        curword -= 1
      #      else:
      #        curword = 0
      #      #vstrmov = len(vstrarr[-1])
      #      screen.move(1,newpos)
      #      #screen.move(3,0)
      #      #screen.addstr(str(vstrarr) + " " + str(curword))
      #      #sy, sx = screen.getyx()
      #      #for i in range(vstrdel):
      #      #  screen.delch()
      if ch == 127 or ch == 263:
        if strlen >= 0:
          vstr = vstr[:-1]
          strlen = len(vstr)
          screen.move(1,strlen)
          screen.delch()
      elif ch == 8: # shift backspace
        if strlen > 1:
          if vstr[-1] == " ":
            vstrdel = 1
          else:
            vstrarr = vstr.split(" ")
            vstrdel = len(vstrarr[-1])
          vstr = vstr[:-vstrdel]
          strlen = len(vstr)
          screen.move(1,strlen)
          for i in range(vstrdel):
            screen.delch()
      else:
        vstr += chr(ch)
        screen.attrset(col["hiGr"])
        if passwd == 1:
          screen.addch("*")
        else:
          screen.addch(chr(ch))
      cury, curx = screen.getyx()
      sy, sx = screen.getyx()
      prev_ch = ch
  curses.curs_set(0)
  return(vstr)


## UNIT TEST
#from py_curses_lib import init_colors
#screen = curses.initscr()
#col = init_colors()
#read_str(screen, col, "test", "select 1 from dual union all select 1", passwd = 0)
#curses.endwin()
