from . import this_your_admin

def main():
	import sys
	import wand.display
	with (
		wand.image.Image(blob=sys.stdin.buffer.read()) as to_insert,
		this_your_admin(to_insert) as out,
	):
		wand.display.display(out)
		out.save(file=sys.stdout.buffer)

if __name__ == '__main__':
	main()
