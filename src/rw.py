import ref, re, eo, time, os

def main():
    
    b = eo.Building()
    b.load('../samples/input/inp/Kendrick.inp')
    b.dump('../samples/output/inp/Kendrick.inp')

if __name__ == "__main__":
    main()


