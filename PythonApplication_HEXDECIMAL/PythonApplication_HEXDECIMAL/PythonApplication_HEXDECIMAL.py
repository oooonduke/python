for i in range(999,10000):
        #k = format(i, 'x')
        #l = int(bin(i & 0B0000000011111111),2)
        l = i & 0B0000000011111111
        if l == 0:
            #print("１０進数は",i,"１６進数は",k)
             print(f"１０進数は {i} １６進数は {i:x}")