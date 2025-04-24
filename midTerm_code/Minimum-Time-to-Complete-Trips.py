class Solution:
    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        timeAcc = 0
        totalTripsAcc = 0
        #create tripesAcc to record finished trips
        tripsAcc = []
        for i in range(len(time)):
            tripsAcc.append(0)
        #create a field
        f = []
        for i in range(len(time)):
            f.append(0)
        #defind a funtion run()
        def run(f,timeAcc):
            timeAcc += 1
            for i in range(len(f)):
                f[i] += 1
            return f,timeAcc
        def check(f,totalTripsAcc):
            for i in range(len(f)):
                if f[i] == time[i]:
                    tripsAcc[i] += 1
                    f[i] = 0
            totalTripsAcc = sum(tripsAcc)
            return f,totalTripsAcc
        while totalTripsAcc < totalTrips:
            f,timeAcc = run(f,timeAcc)
            f,totalTripsAcc = check(f,totalTripsAcc)
        return timeAcc