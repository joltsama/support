'''
Assumption:

Data repeats after a certain time.
For e.g. issue called during moring time has high chances of resolving quickly than the one during night time.
Thus there is a period of 24hrs which repeats.
'''

import datetime
import time
import random


class AgentPredictTime:
    # 24 hrs, 12 intervals of 5 minutes
    # 300 seconds b/w intervals

    # total_intervals = 24*12
    # interval_time = 300

    # for testing purpose, interval time has been reduced to 1 hr
    total_intervals = 24
    interval_time = 3600

    def simulate(self, pred_date):
        new_pred = pred_date[:]
        total_issues = random.randint(10, 20)
        issues = self.generate_issue_data(total_issues)
        for i in issues:
            self.predict_time(i, new_pred)
        return new_pred, issues

    def simplify_issue_time(self, issue):
        t1 = time.strptime(issue[0], '%d-%m-%Y %H:%M:%S')
        t2 = time.strptime(issue[1], '%d-%m-%Y %H:%M:%S')
        s1 = t1.tm_hour*60*60+t1.tm_min*60+t1.tm_sec
        s2 = time.mktime(t2)-time.mktime(t1)
        timevalue = s1 % 86400
        rounded_s1 = timevalue % self.interval_time
        if rounded_s1 < self.interval_time/2:
            timevalue -= rounded_s1
        else:
            timevalue += self.interval_time-rounded_s1
        timevalue = int(timevalue/self.interval_time)
        return (timevalue % self.total_intervals, s2)

    def simplify_issue_time_from_time(self, time_string):
        t1 = time.strptime(time_string, '%H:%M')
        s1 = t1.tm_hour*60*60+t1.tm_min*60+t1.tm_sec
        timevalue = s1 % 86400
        print(timevalue)
        rounded_s1 = timevalue % self.interval_time
        if rounded_s1 < self.interval_time/2:
            timevalue -= rounded_s1
        else:
            timevalue += self.interval_time-rounded_s1
        print(timevalue)
        timevalue = int(timevalue/self.interval_time)
        return timevalue % self.total_intervals

    def resolved(self, issue, pred_date):

        # take average of 10% entries near current entry and change data accordingly
        lookup = int(self.total_intervals*5/100)

        j = 0
        data_sum = 0
        while j < lookup:
            data_sum += pred_date[(issue[0]+j) % self.total_intervals]
            j += 1

        j = 1
        data_sum = 0
        while j < lookup:
            data_sum += pred_date[(issue[0]-j) % self.total_intervals]
            j += 1

        actual_value = issue[1]
        predicted_value = pred_date[issue[0]]
        avg_value = data_sum/(2*lookup)

        # higher value of incf mean predicted and actual are closer.
        # thus predicted value will change rapidly for actual values near it
        # but will change slowly for actual values far from it

        inc_f = min(actual_value, predicted_value) / \
            max(actual_value, predicted_value)

        # inc_f * max(actual_value, predicted_value) ensures the value does not
        # change rapidly in either direction
    
        val = inc_f*max(actual_value, predicted_value) + \
            (1-inc_f)*(0.6*predicted_value+0.4*avg_value)

        pred_date[issue[0]] = float(format(val, '.2f'))

    def predict_time(self, issue, pred_date):
        '''
        predict time with simplification. issue has standard time format
        '''
        issue = self.simplify_issue_time(issue)
        k = pred_date[issue[0]]
        self.resolved(issue, pred_date)
        return k

    def predict_time2(self, issue, pred_date):
        '''
        predict time without simplification. issue has int [start_time, answer_time] format
        '''
        k = pred_date[issue[0]]
        self.resolved(issue, pred_date)
        return k

    def make_pred_data(self):
        return [300, ]*self.total_intervals

    def generate_issue_data(self, size):
        issues = []
        for i in range(size):
            stime = (time.time()+random.randint(0, 60*60*24-1))
            start_time = time.strftime(
                '%d-%m-%Y %H:%M:%S', time.localtime(stime))
            if random.randint(0, 8) < 6:
                answer_time = time.strftime(
                    '%d-%m-%Y %H:%M:%S', time.localtime(stime+random.randint(5, 180)))
            else:
                answer_time = time.strftime(
                    '%d-%m-%Y %H:%M:%S', time.localtime(stime+random.randint(181, 600)))
            issue = (start_time, answer_time)
            issues.append(issue)
        return issues


# ag = AgentPredictTime()
# issues = ag.generate_issue_data(28800)
# pred_data = ag.make_pred_data()
# for issue in issues:
#     ag.predict_time(issue, pred_data)

# print('Val', ag.simplify_issue_time_from_time('00:00'))
# print('Val', ag.simplify_issue_time_from_time('00:30'))
# print('Val', ag.simplify_issue_time_from_time('00:45'))


# dataset,newissues = ag.simulate(7, pred_data)

# for i in range(len(dataset)):
#     print("DAY", i+1)
#     print(dataset[i])

# while 1:
#     a=int(input())
#     b=int(input())
#     if a=='q':
#         break
#     print(ag.predict_time2([a,b], pred_data))
