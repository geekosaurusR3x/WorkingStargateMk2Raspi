for i in range(9):
    print('<div class="chevron" num="{0}" id="chevron{1}"><img src="chevrons/00{1}.svg" /></div>'.format(i, i + 1, i + 1))

for i in range(9, 39):
    print('<div class="chevron" num="{0}" id="chevron{1}"><img src="chevrons/0{1}.svg" /></div>'.format(i, i + 1, i + 1))
