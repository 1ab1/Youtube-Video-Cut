from multiprocessing.pool import ThreadPool


def helper(args):
    #print args
    return prod(*args)

def prod(a, b):
    print a+b

arr = [(1,2), (6,7)]
results = ThreadPool(3).map(helper, arr)


url = 'https://www.youtube.com/watch?v=OkSceILd-qQ'
url = 'https://www.youtube.com/watch?time_continue=3490&v=Y_51wKtAnWI'
print url.split('v=')[1].split('&')[0]



def refine_inervs(intervals):
    final_intervals = []
    for interval in intervals:
        arr = []
        start = int(interval[0])
        end = int(interval[1])
        print start, end
        while end - start > 600:
            arr.append(str(start))
            arr.append(str(start+600))
            final_intervals.append(arr)
            start = start + 600
            arr = []
        arr.append(str(start))
        arr.append(str(end))
        final_intervals.append(arr)
    return final_intervals

print refine_inervs([['1774', '4551']])