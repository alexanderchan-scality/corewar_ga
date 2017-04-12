#!/usr/bin/python

import os
import re
import sys
import glob
import time
import random
import subprocess
import numpy as np

MIN_LINES = 5
CROSS_PER = 0.05
ELITE_NUM = 16
CROSS_NUM = 14
MTATE_NUM = 10

MAX_CHAMPS = 5
MAX_LINES = 250

asm_path = "./asm"
corewar_path = "./corewar"

MAX_INT = 2147483647
MIN_INT = -2147483648

def sp_rand(mx):
    lim=mx*(mx-1)/2
    a=random.randint(0,lim)
    for i in range(mx):
        if (a <=(i*(i+1)/2)):
            return i
    print ("not possible")
    return (lim)

def random_line():
    reg = [random.randint(1, 16) for i in range(3)]
    num = [random.randint(MIN_INT, MAX_INT) for i in range(3)]
    rand_type = random.randint(1, 25)

    if (rand_type == 1):
        return ("add r%d,r%d,r%d\n" % (reg[0], reg[1], reg[2]))
    if (rand_type == 2):	
        return ("aff r%d\n" % (reg[0]))
    if (rand_type == 3):
        return ("and %%%d,%%%d,r%d\n" % (num[0], num[1], reg[2]))
    if (rand_type == 4):
        return ("and r%d,%%%d,r%d\n" % (reg[0], num[1], reg[2]))
    if (rand_type == 5):
        return ("fork %%%d\n" % (num[0]))
    if (rand_type == 6):
        return ("ld %%%d,r%d\n" % (num[0], reg[1]))
    if (rand_type == 7):
        return ("ld %d,r%d\n" % (num[0], reg[1]))
    if (rand_type == 8):
        return ("ldi %%%d,%%%d,r%d\n" % (num[0], num[1], reg[2]))
    if (rand_type == 9):
        return ("ldi %%%d,r%d,r%d\n" % (num[0], reg[1], reg[2]))
    if (rand_type == 10):
        return ("lfork %%%d\n" % (num[0]))
    if (rand_type == 11):
        return ("live %%%d\n" % (num[0]))
    if (rand_type == 12):
        return ("lldi %%%d,%%%d,r%d\n" % (num[0], num[1], reg[2]))
    if (rand_type == 13):
        return ("or %d,%%%d,r%d\n" % (num[0], num[1], reg[2]))
    if (rand_type == 14):
        return ("or r%d,r%d,r%d\n" % (reg[0], reg[1], reg[2]))
    if (rand_type == 15):
        return ("st r%d,%d\n" % (reg[0], num[1]))
    if (rand_type == 16):
        return ("st r%d,r%d\n" % (reg[0], reg[1]))
    if (rand_type == 17):
        return ("sti r%d,%%%d,%%%d\n" % (reg[0], num[1], num[2]))
    if (rand_type == 18):
        return ("sti r%d,%%%d,r%d\n" % (reg[0], num[1], reg[2]))
    if (rand_type == 19):
        return ("sti r%d,r%d,%%%d\n" % (reg[0], reg[1], num[2]))
    if (rand_type == 20):
        return ("sti r%d,r%d,r%d\n" % (reg[0], reg[1], reg[2]))
    if (rand_type == 21):
        return ("sub r%d,r%d,r%d\n" % (reg[0], reg[1], reg[2]))
    if (rand_type == 22):
        return ("xor r%d,%%%d,r%d\n" % (reg[0], num[1], reg[2]))
    if (rand_type == 23):
        return ("xor r%d,r%d,r%d\n" % (reg[0], reg[1], reg[2]))
    if (rand_type == 24):
        return ("zjmp %d\n" % (num[0]))
    return ("\n")

class Champion:

    def __init__(self, gid, cid):
        self.cid = cid
        if (gid >= 0):
            self.name = 'gen_%d_id_%d' % (gid, cid)
            self.path = './gen_%d/gen_%d_id_%d.s' % (gid, gid, cid)
            self.exe = './gen_%d/gen_%d_id_%d.cor' % (gid, gid, cid)
        else:
            self.name = 'test_%d' % (cid)
            self.path = './test_files/test_%d.s' % (cid)
            self.exe = './test_files/test_%d.cor' % (cid)
        self.code = []

    def make_lines(self):
        with open(self.path, 'w') as ofile:
            ofile.write(".name \"" + self.name + "\"\n")
            ofile.write(".comment \"" + self.name + "\"\n")
            for line in range(MAX_LINES):
                self.code.append(line)
                ofile.write(self.name + " " + str(line) +"\n")

    def take_lines(self, cross_lines):
        with open(self.path, 'w') as ofile:
            ofile.write(".name \"" + self.name + "\"\n")
            ofile.write(".comment \"" + self.name + "\"\n")
            for line in cross_lines:
                self.code.append(line)
                ofile.write(line)

    def compile(self):
        cmd = [asm_path, self.path]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            return (stdout, stderr, proc.returncode)
        except:
            return ("", "", 1)

    def who_won(self, s):
        p = re.search('player (\d)\(.*\) won', s)
        try:
            val = p.group(1)
            print (p.group(0))
            # print int(val) - 1
            return int(val) - 1
        except:
            print ("No winner in given conditions")
            return 2

    def count_finished(self, procs):
        count = 0
        finished = 0
        for proc in procs:
            count +=1
            if (proc.poll()!=None):
                finished += 1
        print ("finished %d / %d"%(finished, count))
        return ((finished/float(count)) if count else 0) 


    def fight_group(self, list_of_enemies, thresh, timeout):
        procs = []
        count = 0
        for enemy_pair in list_of_enemies:
            if (count % 100) == 0:
                print ("loading fights {}".format(count))
            command = [corewar_path, enemy_pair[0].exe, enemy_pair[1].exe]
            proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            procs.append(proc)
            count += 1
        deadline = time.time() + timeout
        poll_seconds = 1
        flag = True
        while (time.time() < deadline and flag):
            time.sleep(poll_seconds)
            print ("time: %f"%(time.time()))
            flag = (self.count_finished(procs) < thresh)

        res=[]
        for proc in procs:
            if (proc.poll()==None):
                res.append(2)
                proc.terminate()
            else:
                stdout, stderr = proc.communicate()
                try:
                    res.append(self.who_won(stdout))
                except:
                    res.append(2)
        return res

    def fight(self, enemy, timeout=10):
        command = [corewar_path, self.exe, enemy.exe]
        proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        poll_seconds = .250
        t_out = 0
        deadline = time.time() + timeout
        while (time.time() < deadline and proc.poll() == None):
                time.sleep(poll_seconds)
        if (proc.poll() == None):
            if (float(sys.version[:3]) >= 2.6):
                proc.terminate()
                t_out = 1
        stdout, stderr = proc.communicate()
        return (stdout, stderr, proc.returncode, t_out)

    def mutate(self):
        new_lines = self.code
        num_actions = int(CROSS_PER * len(new_lines))
        num_actions = num_actions if num_actions > MIN_LINES else MIN_LINES
        while (num_actions):
            rand_action = random.randint(0, 2)

            rand_ind = random.randint(0, len(new_lines) - 1)
            line = random_line()
            if (rand_action == 0 and len(new_lines) > 5):
            #delete
                del new_lines[rand_ind]
                num_actions -= 1
            elif (rand_action == 1):
            #insert
                new_lines.insert(rand_ind, line) 
                num_actions -= 1
            elif (rand_action == 2):
            #swap
                new_lines[rand_ind] = line
                num_actions -= 1
        return (new_lines)	

    def crossover(self, partner):
        self_lines, part_lines = self.code, partner.code
        num_actions = int(CROSS_PER * len(part_lines))
        num_actions = num_actions if num_actions > MIN_LINES else MIN_LINES
        while (num_actions):
            rand_action = random.randint(0, 2)

            rand_ind = random.randint(0, len(part_lines) - 1)
            rand_ind_2 = random.randint(0, len(self_lines) - 1)
            if (rand_action == 0 and len(part_lines) > 5):
            #delete
                del part_lines[rand_ind]
                num_actions -= 1
            elif (rand_action == 1):
            #insert
                part_lines.insert(rand_ind, self_lines[rand_ind_2])
                num_actions -= 1
            elif (rand_action == 2):
            #swap
                part_lines[rand_ind] = self_lines[rand_ind_2]
                num_actions -= 1
        return (part_lines)	

class Generation:

    def __init__(self, gid):
        self.gid = gid
        self.champ_list = []
        if (gid >= 0):
            self.folder = './gen_%d/' % gid
        else:
            self.folder = './test_files/'
        if (not os.path.exists(self.folder)):
            os.mkdir(self.folder)

    def make_champ(self):
        for cid in range(MAX_CHAMPS):
            new_contender = Champion(self.gid, cid + 1)
            new_contender.make_lines()
            self.champ_list.append(new_contender)

    def load_champ(self, path):
        files = glob.glob(path + "*.s")
        files.sort()
        cid = 1
        pedigree = []
        for f in files:
            new_contender = Champion(self.gid, cid)
            lines = None
            with open(f, 'r') as ifile:
                lines = [line for line in ifile]	
            new_contender.take_lines(lines[2:])
            pedigree.append(f + " --> " + new_contender.name)
            self.champ_list.append(new_contender)
            cid += 1
        with open(self.folder + "tree.txt", 'w') as ofile:
            for i in pedigree:
                ofile.write(i + "\n")

    def add_champion(self, champion):
        self.champ_list.append(champion)

    def compile_gen(self):
        for champ in self.champ_list:
            champ.compile()

    def isbest(self, old_champ):
        for champ in self.champ_list:
            for old_champ_i in old_champ:
                print (champ.name, "vs", old_champ_i.name)
                res = champ.fight(old_champ_i, 10)
                if (res[3] == 0):
                    m = re.search('player (\d)\(.*\) won', res[0])
                    try:
                        if (m.group(1) == '1'):
                            res2 = old_champ_i.fight(champ, 10)
                            if (res2[3] == 0):
                                m = re.search('player (\d)\(.*\) won', res2[0])
                                if (m.group(1) == '2'):
                                    print ("%s beats %s"%(i.name, old_champ_i.name))
                                    return (True)
                    except:
                        print ("Exception raised")
                        pass
        print ("We can't beat the current champion")
        return (False)
    
    def getMetric(self, test_gen):
        fight_list = []
        for i in self.champ_list:
            for j in test_gen.champ_list:
                fight_list.append((i, j))
        res_list = self.champ_list[0].fight_group(fight_list, .9, 10)
        total = 0
        flag = False
        for res in res_list:
            if res_list[res] == 0:
                total += 1
        print ("Metric for generation %d potential: %d / %d" %
                (self.gid, total, len(fight_list)))

    def fight(self):
        print (str(self.gid) + " fighting!!")
        l = len(self.champ_list)
        t = (l * l - l) / 2
        c = 0
        self.score = np.zeros((l, l))
        fight_list = []
        for i in range(1, l):
            for j in range(i):
                fight_list.append((self.champ_list[i], self.champ_list[j]))
        res_list = self.champ_list[0].fight_group(fight_list, .9, 10)
        total = 0
        for res in range(len(res_list)):
            if res_list[res] == 0:
                total += 1
                self.score[fight_list[res][0].cid - 1,fight_list[res][1].cid - 1] = 1
            elif res_list[res] == 1:
                self.score[fight_list[res][1].cid - 1,fight_list[res][0].cid - 1] = 1
            print("win count %d / %d"%(total, len(res_list)))
        self.score.dump(self.folder + "scores_d.dat")


    def next_generation(self):
        next_gid = self.gid + 1
        next_gen = Generation(next_gid)

        
        print "read rank file"
        ar = np.load(self.folder + "scores_d.dat")
        ar = np.sum(ar, axis=1)
        ar = ar.tolist()
        matched_list = [(self.champ_list[i], ar[i]) for i in range(len(ar))]
        matched_list.sort(key=lambda x: x[1])

        pedigree = []

        cid = 1
        print ("select "+str(ELITE_NUM)+" champs as elite members")
        elite_list = [elite[0] for elite in matched_list[-ELITE_NUM:]]
        for i in elite_list:
            new_contender = Champion(next_gid, cid)
            new_contender.take_lines(i.code)
            next_gen.champ_list.append(new_contender)
            cid += 1
            pedigree.append("Elite " + i.name + " --> " + new_contender.name)

        cross_list = []
        cross_count = 0
        while (cross_count < CROSS_NUM):
            print "trying to creat new guy #", str(cross_count)
            try_cnt = 0
            bot_1 , bot_2 = 0, 0
            while (bot_1 == bot_2):
                bot_1 = sp_rand(len(self.champ_list)) - 1
                bot_2 = sp_rand(len(self.champ_list)) - 1
            bot_1 = self.champ_list[bot_1]
            bot_2 = self.champ_list[bot_2]
            c_able = False
            new_contender = None
            while (not c_able) and (try_cnt < 10):
                new_contender = Champion(next_gid, cid)
                new_contender.take_lines(bot_1.crossover(bot_2))
                _1, _2, res = new_contender.compile()
                # print (_1, _2, res)
                if (not res):
                    c_able = True
                    next_gen.champ_list.append(new_contender)
                    cid += 1
                    cross_count += 1
                    pedigree.append("Cross " + bot_1.name + " +  " + bot_2.name + " --> " + new_contender.name)
                else:
                    try_cnt += 1
                    new_contender = None

        #mutation
        mut_count = 0
        while (mut_count < MTATE_NUM):
            print "trying to create guy #"+str(mut_count)+" by mutation"
            try_cnt = 0
            bot_1 = sp_rand(len(self.champ_list))
            print ("bot_1 %d"%(bot_1))
            bot_1 = self.champ_list[bot_1]
            new_contender = None
            c_able = False
            while (not c_able and try_cnt<10):
                new_contender = Champion(next_gid, cid)
                new_contender.take_lines(bot_1.mutate())
                _1, _2, res = new_contender.compile()
                if (not res):
                    c_able = True
                    next_gen.champ_list.append(new_contender)
                    cid += 1
                    mut_count += 1
                    pedigree.append("Mutate " + bot_1.name + " --> " + new_contender.name)
                else:
                    try_cnt += 1
                    new_contender = None

        with open(next_gen.folder + "tree.txt", 'w') as ofile:
            for i in pedigree:
                ofile.write(i + "\n")
            
        print "New generation is ready"
        return (next_gen)

