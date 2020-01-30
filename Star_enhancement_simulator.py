import random
import math
from flask import Flask, render_template

millnames = ['',' Thousand',' Million',' Billion',' Trillion']
suc_rate= [(0,1,0.95,0.05,0.0),(1,2,0.90,0.10,0.0),(2,3,0.85,0.15,0.0),
           (3,4,0.85,0.15,0.0),(4,5,0.80,0.20,0.0),(5,6,0.75,0.25,0.0),
           (6,7,0.70,0.30,0.0),(7,8,0.65,0.35,0.0),(8,9,0.60,0.40,0.0),
           (9,10,0.55,0.45,0.0),
           (10,11,0.5,0.5,0.0),(11,12,0.45,0.55,0.0),(12,13,0.40,0.594,0.06),(13,14,0.35,0.637,0.013),
           (14,15,0.30,0.686,0.014),(15,16,0.30,0.679,0.021),(16,17,0.30,0.679,0.021),
           (17,18,0.30,0.679,0.021),(18,19,0.30,0.672,0.028),(19,20,0.30,0.672,0.028),
           (20,21,0.30,0.63,0.07 ),(21, 22, 0.30, 0.63,0.07),
           (22, 23, 0.03, 0.776, 0.194),
           (23, 24, 0.02, 0.686, 0.294),(24,25, 0.01,0.594,0.396)]
def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.4f}{}'.format(n / 10**(3 * millidx), millnames[millidx])



def find_rate (lst,star):
    result = -1
    for item in lst:
        if star == item[0]:
            result = item
    return result

def find_suc_rate (lst, current_start, next_star):
    result = -1
    for item in lst:
        if current_start == item[0] and next_star == item[1]:
            result = item
    return result

def get_rate():
    return random.random()

def get_cost(level,current_star,discount):
    cost = -1
    if 0 <= current_star < 10:
        cost =(1000 + ((level**3) * ((current_star+1)**2.7))/25.) * discount
    elif 10 <= current_star < 15 :
        cost = (1000 + ((level**3) * ((current_star+1)**2.7))/400.) * discount
    elif 15 <= current_star < 18:
        cost = (1000 + ((level**3) * ((current_star+1)**2.7))/120.)* discount
    elif 18 <= current_star < 20:
        cost = (1000 + ((level**3) * ((current_star+1)**2.7))/110.)* discount
    elif 20 <= current_star <=24:
        cost = (1000 + ((level ** 3) * ((current_star + 1) ** 2.7))/110.)*discount
    else:
        print("Wrong star input~")
    return cost

def star_catch(s_rate, f_rate, d_rate):
    s_rate = s_rate + 0.045
    total = s_rate+f_rate+d_rate
    rs_rate = s_rate/total
    rf_rate = f_rate/total
    d_rate = d_rate/total
    return (rs_rate,rf_rate,d_rate)


def enhance_func(current_star, next_star, guard, star_catcher):
    rate_flag = get_rate()
    rate_info = find_suc_rate(suc_rate, current_star, next_star)
    if  star_catch == True:
        temp_rate = star_catch(rate_info[2],rate_info[3],rate_info[4])
        sucess_rate = temp_rate[0]
        fail_rate = temp_rate[1]
        destory_rate = temp_rate[2]
    else:
        sucess_rate = rate_info[2]
        fail_rate = rate_info[3]
        destory_rate = rate_info[4]
    final_star = current_star
    if 0 <= next_star <= 10:
       if rate_flag <= sucess_rate:
           final_star += 1
       elif rate_flag > sucess_rate:
           final_star = current_star
    elif 11 <= next_star <= 12:
       if next_star == 11:
           if rate_flag <= sucess_rate:
               final_star += 1
           elif rate_flag > sucess_rate:
               final_star = 10
       else:
           if rate_flag <= sucess_rate:
               final_star += 1
           elif rate_flag > sucess_rate:
               final_star = final_star - 1
    elif 12 <= current_star <= 17 and guard == True:
       if next_star == 16:
           if rate_flag <= sucess_rate:
               final_star += 1
           elif rate_flag > sucess_rate:
               final_star = 15
       else:
           if rate_flag <= sucess_rate:
               final_star +=1
           elif rate_flag > sucess_rate:
               final_star = final_star - 1
    elif 12 <= current_star <= 17 and guard == False:
        if next_star == 16:
            if rate_flag <= sucess_rate:
                final_star += 1
            elif sucess_rate <rate_flag <= sucess_rate + fail_rate:
                final_star = 15
            elif rate_flag > sucess_rate + fail_rate:
                final_star = -1
        else:
            if rate_flag <= sucess_rate:
                final_star += 1
            elif sucess_rate <rate_flag <= sucess_rate + fail_rate:
                final_star = final_star - 1
            elif rate_flag > sucess_rate + fail_rate:
                final_star = -1
    elif 18 <= current_star <= 25:
        if next_star == 21:
            if rate_flag <= sucess_rate:
                final_star += 1
            elif sucess_rate <rate_flag <= sucess_rate + fail_rate:
                final_star = 20
            elif rate_flag > sucess_rate + fail_rate:
                final_star = -1
        else:
            if rate_flag <= sucess_rate:
                final_star += 1
            elif sucess_rate <rate_flag <= sucess_rate + fail_rate:
                final_star = final_star - 1
            elif rate_flag > sucess_rate + fail_rate:
                final_star = -1
    return final_star


def enhancement(item_level, initial_star, final_star, discount,guard,star_catcher):
    current_star = initial_star
    next_star = initial_star + 1
    current_cost = 0
    total_cost = 0
    total_trials = 0
    drop_fail = 0
    while (current_star < final_star):
        current_cost = get_cost(item_level, current_star, discount)
        result_star = enhance_func(current_star,next_star,guard,star_catcher)
        if result_star == next_star:
            current_star = next_star
            next_star = current_star + 1
            drop_fail = 0
        elif result_star == current_star:
            current_star = current_star
            next_star = current_star + 1
            drop_fail = 0
        elif result_star == current_star - 1:
            current_star = current_star -1
            next_star = current_star + 1
            drop_fail += 1
        #chance Time
        if drop_fail - 2 == 0:
            drop_fail = 0
            current_star = next_star
            next_star = current_star + 1
            total_cost += get_cost(item_level,current_star,discount)
            total_trials += 1
        if guard == True:
            if 13 <= result_star <=17:
              total_cost += current_cost * 2
        else:
            total_cost += current_cost
        total_trials += 1
        if result_star == -1:
            return(result_star,total_trials,total_cost)
        if result_star == final_star:
            return (result_star, total_trials,total_cost)

def generator(level, initial_star, final_star, discount, guard,star_catcher, item_num):
    total_cost = list()
    item_destoried = 0
    for i in range(0,item_num):
        item_info = enhancement(level,initial_star,final_star,discount,guard,star_catcher)
        total_cost.append(item_info[-1])
        if item_info[0] == -1:
            item_destoried += 1
    avg_cost = sum(total_cost) / item_num
    lowest_cost = min(total_cost)
    highest_cost = max(total_cost)
    print("===================================================================")
    print("Avg cost of %s level %d enhancement is %s mesos" % (level, final_star, millify(avg_cost)))
    print("Lowest cost : %s ||| Highest cost: %s " % (millify(lowest_cost), millify(highest_cost)))
    print("Destoried items : ", item_destoried)
    print("Overall successful rate is : ", (item_num - item_destoried) / item_num)

def main():
   generator(160,0,17,0.95,True,True,10000)
   generator(160,0,17,0.95,False,False,10000)
main()

