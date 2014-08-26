import ref, re, eo, time, os

def main():
    
    b = eo.Building()
    b.load('../samples/input/inp/Kendrick.inp')

    iw = b.objects['"2-ELEC_P-I3+3-222"']
    print iw.zone().name

    b.dump('../samples/output/inp/Kendrick.inp')

if __name__ == "__main__":
    main()


