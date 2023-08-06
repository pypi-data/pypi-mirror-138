

def print_lol(the_list):
  for item in the_list:
    if isinstance(item, list):
      print_lol(item)
    else:
      print(item)   


def print_lol_indent (the_list,indent=False, level=0):
  for m in the_list:
    if isinstance(m, list):
      print_lol(m, indent, level + 1)
    else:
      if indent:
        for tab_stop in range(level):
          print("\t", end='')
      print(m)

