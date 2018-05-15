import matplotlib.pyplot as plt

delim_time = "@Time:"
delim_quality = ", quality = "
delim_tput = ", throughput = "
delim_rebuf1 = ", rebuffering: "
delim_rebuf2 = "<->"
filename_1 = "c1-05100843-6mbps"
filename_2 = "c2-05100843-6mbps"
wireshark_time = 1525999211190
offset = 50000

def parse_quality(line, delim1, delim2, time, quality, all_time, all_quality):
    time = int(line[line.find(delim1)+len(delim1) : line.find(delim2)])
    all_time.append(time)
    all_quality.append(quality)
    quality = int(line[line.find(delim2)+len(delim2) : ])
    all_time.append(time)
    all_quality.append(quality)
    return time, quality

def parse_tput(line, delim1, delim2, time, tput, all_time, all_tput):
    time = int(line[line.find(delim1)+len(delim1) : line.find(delim2)])
    tput = line[line.find(delim2)+len(delim2) : ]
    if 'NaN' in tput:
        tput = 0
    else:
        tput = float(tput)
    all_time.append(time)
    all_tput.append(tput)
    return time, tput

#def parse_rebuf(line, delim1, delim2, all_time, all_rebuf):
#    rebuf_start = float(line[line.find(delim1)+len(delim1) : line.find(delim2)])
#    rebuf_end = float(line[line.find(delim2)+len(delim2) : ])
#    print(rebuf_start)
#    print(rebuf_end)    
#    all_time.append(rebuf_start)
#    all_rebuf.append(0)
#    all_time.append(rebuf_start)
#    all_rebuf.append(1)
#    all_time.append(rebuf_end)
#    all_rebuf.append(1)
#    all_time.append(rebuf_end)
#    all_rebuf.append(0)

def parse_rebuf(line, delim1, delim2, all_time, all_rebuf, all_time_rebuf_cnt):
    rebuf_start = int(float(line[line.find(delim1)+len(delim1) : line.find(delim2)]))
    rebuf_end = int(float(line[line.find(delim2)+len(delim2) : ]))
    all_time += list(range(rebuf_start, rebuf_end, 100))
    all_time_rebuf_cnt.append((rebuf_end - rebuf_start)/1000)
    
all_time_1 = [wireshark_time] 
all_time_quality_1 = [0]
all_time_2 = [wireshark_time] 
all_time_quality_2 = [0]
time1 = 0
time2 = 0
quality1 = 0
quality2 = 0
all_time_3 = [wireshark_time] 
all_time_tput_3 = [0]
all_time_4 = [wireshark_time] 
all_time_tput_4 = [0]
time3 = 0
time4 = 0
tput3 = 0
tput4 = 0
all_time_5 = [] 
all_time_rebuf_5 = []
all_time_rebuf_cnt_5 = []
all_time_6 = [] 
all_time_rebuf_6 = []
all_time_rebuf_cnt_6 = []
time5 = 0
time6 = 0
rebuf5 = 0
rebuf6 = 0
                
with open(filename_1) as file:
    for line in file:
        if delim_quality in line:
            time1, quality1 = parse_quality(line, delim_time, delim_quality, time1, quality1, all_time_1, all_time_quality_1)
        elif delim_tput in line:
            time3, tput3 = parse_tput(line, delim_time, delim_tput, time3, tput3, all_time_3, all_time_tput_3)
        elif delim_rebuf1 in line:
            parse_rebuf(line, delim_rebuf1, delim_rebuf2, all_time_5, all_time_rebuf_5,all_time_rebuf_cnt_5)
            
with open(filename_2) as file:
    for line in file:
        if delim_quality in line:
            time2, quality2 = parse_quality(line, delim_time, delim_quality, time2, quality2, all_time_2, all_time_quality_2)
        elif delim_tput in line:
            time4, tput4 = parse_tput(line, delim_time, delim_tput, time4, tput4, all_time_4, all_time_tput_4)
        elif delim_rebuf1 in line:
            parse_rebuf(line, delim_rebuf1, delim_rebuf2, all_time_6, all_time_rebuf_6, all_time_rebuf_cnt_6)
            
max_time = max(all_time_1 + all_time_2 + all_time_3 + all_time_4 + all_time_5 + all_time_6)

all_time_1.append(max_time)
all_time_quality_1.append(quality1)
all_time_2.append(max_time)
all_time_quality_2.append(quality2)

all_time_1 = [(x - wireshark_time)/1000 for x in all_time_1]
all_time_2 = [(x - wireshark_time - offset)/1000 for x in all_time_2]
all_time_3 = [(x - wireshark_time)/1000 for x in all_time_3]
all_time_4 = [(x - wireshark_time - offset)/1000 for x in all_time_4]
all_time_5 = [(x - wireshark_time)/1000 for x in all_time_5]
all_time_6 = [(x - wireshark_time - offset)/1000 for x in all_time_6]

all_time_rebuf_5 = [1] * len(all_time_5)
all_time_rebuf_6 = [1] * len(all_time_6)

fig, ax1 = plt.subplots()
line1, = ax1.plot(all_time_1, all_time_quality_1, 'b')
line2, = ax1.plot(all_time_2, all_time_quality_2, 'r')
ax1.set_xlabel('time (s)')
ax1.xaxis.set_ticks(range(0,540,15))
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('quality')
ax1.yaxis.set_ticks(range(20))
ax1.tick_params('y')

#ax2 = ax1.twinx()
#ax2.plot(all_time_3, all_time_tput_3, 'b-.')
#ax2.plot(all_time_4, all_time_tput_4, 'r-.')
#ax2.set_ylabel('throughput')
#ax2.tick_params('y')

#ax2 = ax1.twinx()
#ax2.stackplot(all_time_5, all_time_rebuf_5, color = 'b')
#ax2.stackplot(all_time_6, all_time_rebuf_6, color = 'r')
#ax2.set_ylabel('rebuffering')
#ax2.yaxis.set_ticks([-100,0,1,101])
#ax2.yaxis.set_ticklabels(['','OFF','ON',''])
#ax2.tick_params(axis='y', direction='out', length=6, width=2, colors='k')

ax2 = ax1.twinx()

ax2.plot(all_time_6, all_time_rebuf_6, 'ro')
ax2.plot(all_time_5, all_time_rebuf_5, 'bo')
ax2.set_ylabel('rebuffering')
ax2.yaxis.set_ticks([0,1,2])
ax2.yaxis.set_ticklabels(['OFF','ON',''])
ax2.tick_params(axis='y', direction='out', length=6, width=2, colors='k')


plt.legend(handles = [line1, line2], labels = ['Client 1', 'Client 2'], bbox_to_anchor=(0.3, 1.01, 0.7, 0.01), loc=3,
           ncol=2, borderaxespad=0)

fig.tight_layout()
plt.show()