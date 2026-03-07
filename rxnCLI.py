import time
import random
import statistics
import sys
import select
import os

def DetectFalseStart():
    ready, _, _ = select.select([sys.stdin], [], [], 0)
    return bool(ready)

def FlushInputBuffer():
    sys.stdin.readline()

R=3

stopwatch=[]

while len(stopwatch)<R: 
    T=random.uniform(2,5)

    print(f"\n{len(stopwatch)+1}/{R}")

    x=input("\n\033[3mpress enter\033[0m\n").lower()
    if x in ["exit", "e", "quit", "q"]:
        print()
        break

    time.sleep(1)
    if DetectFalseStart():
        FlushInputBuffer()
        continue

    print('🔴\n')
    os.system("afplay -v 0.25 redbeep.wav &")
    time.sleep(1.5)
    if DetectFalseStart():
        FlushInputBuffer()
        continue

    print('🔴 🔴\n')
    os.system("afplay -v 0.25 redbeep.wav &")
    time.sleep(1.5)
    if DetectFalseStart():
        FlushInputBuffer()
        continue 

    print('🔴 🔴 🔴\n')
    os.system("afplay -v 0.25 redbeep.wav &")
    time.sleep(T)
    if DetectFalseStart():
        print("False Start\n")
        FlushInputBuffer()
        break

    print('🟢 🟢 🟢')
    os.system("afplay -v 0.25 greenbeep.wav &")

    start=time.time()
    input()
    end=time.time()

    rxnT=(end-start)

    stopwatch.append(rxnT)

    print('_'*14,'\n')
    print(f"{round(rxnT*1000)} ms")
    print('_'*14)

    time.sleep(1)
    if DetectFalseStart():
        FlushInputBuffer()

else:
    if len(stopwatch)>1:
        avg=sum(stopwatch)/len(stopwatch)
        std=statistics.stdev(stopwatch)
        if avg!=0:
            cons=100-100*(std/avg)
        else:
            cons=100
        
        if avg<0.22:
            x='⚡️'
        elif avg<0.26:
            x='🚀'
        elif avg<0.30:
            x='🦅'
        elif avg<0.34:
            x='🐇'
        else:
            x='🐢'

        date=time.strftime("%d/%m/%Y")

        with open("rxnCLI.txt", "r+") as f:
            H=f.readlines()
            if H==[]:
                f.write(date+'|'+str(avg)+'\n')
            else:
                last_entry=float(((H[-1].strip()).split('|'))[1])
                if avg<last_entry:
                    f.write(date+'|'+str(avg)+'\n')
            f.seek(0)
            uH=f.readlines()
            pr=float(((uH[-1].strip()).split('|'))[1])
            prdate=((uH[-1].strip()).split('|'))[0]

        print('_'*14)

        print(f"\nAverage:          {round(avg*1000)} ms {x}")
        print(f"Fastest:          {round(min(stopwatch)*1000)} ms")
        print(f"Consistency:      {round(cons,2)}%\n")

        print(f"Personal record:  {round(pr*1000)} ms  - {prdate}\n")


#CarbonLogic
