import ref, re, eo, time, os

def main():

    b = eo.Building()
    b.load('Roland_Park.inp')
    b.dump('Roland_Park_.inp')

if __name__ == "__main__":
    main()


