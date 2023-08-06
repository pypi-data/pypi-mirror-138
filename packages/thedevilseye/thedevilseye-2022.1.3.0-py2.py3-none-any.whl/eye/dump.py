import logging
from eye import colors

def dump(args,soup):
    with open(args.dump, 'w') as file:
        file.write(soup.ol.get_text())
        file.close()
    if args.verbose:
    	logging.info(f'{colors.white}Output dumped to {colors.green}{args.dump}{colors.reset}')
    	