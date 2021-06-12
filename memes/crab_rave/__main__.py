import tempfile
from .. import crab_rave

def main():
	import sys
	text = ' '.join(sys.argv[1:])
	crab_rave(text, tempfile.mktemp(suffix='.mp4'))

if __name__ == '__main__':
	main()
