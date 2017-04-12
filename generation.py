#!/usr/bin/python

import os
import re
import sys
import glob
import time
import random
import subprocess
import numpy as np

ELITE_NUM = 16
CROSS_NUM = 22
MTATE_NUM = 2

MAX_CHAMPS = 5
MAX_LINES = 250

asm_path = "./asm"
corewar_path = "./corewar"

MAX_INT = 2147483647
MIN_INT = -2147483648

def sp_rand(mx):
    lim=mx*(mx+1)/2
    a=random.randint(0,lim)
    for i in range(mx+1):
        if (a <=(i*(i+1)/2)):
            return i
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
        self.name = 'gen_%d_id_%d' % (gid, cid)
        self.path = './gen_%d/gen_%d_id_%d.s' % (gid, gid, cid)
        self.exe = './gen_%d/gen_%d_id_%d.cor' % (gid, gid, cid)
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
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return (stdout, stderr, proc.returncode)

# regex here to find out who won
    def who_won(self, s):
        p = re.search('player (\d)\(.*\) won', s)
        try:
            val = p.group(1)
            print (p.group(0))
            # print int(val) - 1
            return int(val) - 1
        except:
            print ("can't run corewar")
            return 2

# return percentage of finished procs
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
            
        deadline = time.time() + timeout
        procs = []
        for enemy in list_of_enemies:
            command = [corewar_path, self.exe, enemy.exe]
            proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            procs.append(proc)

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
        proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, strderr=subprocess.PIPE)
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
        line = random_line()
        if (random.randint(0,1) or len(new_lines) >= 250 ):
            mutate_ind = random.randint(0, len(new_lines) - 1)
            new_lines[mutate_ind] = line
        else:
            in_loc = random.randint(0, len(new_lines) - 1)
            new_lines.insert(in_loc, line)
        return(new_lines)

    def crossover(self, partner):
        self_lines, part_lines = self.code, partner.code
        line_swapped = []
        line_nswap = [i for i in range(0, len(part_lines))]
        percent = 0.0
        while (percent < .05):
            rand_ind = random.randint(0,len(line_nswap) - 1)
            rand_line = line_nswap[rand_ind]
            line_nswap.remove(rand_line)
            line_swapped.append(rand_line)
            if (len(self_lines) - 1 < rand_line):
                part_lines[rand_line] = "\n"
            else:
                # print (self_lines[rand_line])
                part_lines[rand_line] = self_lines[rand_line]
            percent = len(line_swapped) / float(len(part_lines))
        return (part_lines)	

class Generation:

    def __init__(self, gid):
        self.gid = gid
        self.champ_list = []
        self.folder = './gen_%d/' % gid
        if (not os.path.exists(self.folder)):
            os.mkdir(self.folder)

    def make_champ(self):
        for cid in range(MAX_CHAMPS):
            new_contender = Champion(self.gid, cid + 1)
            new_contender.make_lines()
            self.champ_list.append(new_contender)

    def load_champ(self, path):
        files = glob.glob(path + "*.s")
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
        res_1, res_2 = False, False
        final_res = True
        for champ in self.champ_list:
            for old_champ_i in old_champ:
                print (champ.name, "vs", old_champ_i.name)
                res = champ.fight(old_champ_i, 10)
                if (res[3] == 0):
                    m = re.search("Contestant (\d),.*, has won", res[0])
                    if (m.group(1) == '1'):
                        res_1 = True
                res2 = old_champ_i.fight(champ, 10)
                if (res2[3] == 0):
                    m = re.search("Contestant (\d),.*, has won", res2[0])
                    if (m.group(1) == '1'):
                        res_2 = True
                if ((res_1) and (res_2)) or ((not res_1) and (not res_2)):
                    final_res = False
                elif (res_1):
                    print (champ.name)
                    return (True)
        return (final_res)

    def fight(self):
        print (str(self.gid) + " fighting!!")
        l = len(self.champ_list)
        t = (l * l - l) / 2
        c = 0
        self.score = np.zeros((l, l))
        for i in range(l):
            enemy_list = []
            print ("{}".format(self.champ_list[i].name))
            for j in range(l):
                if (j != i):
                    enemy_list.append(self.champ_list[j])
            res_list = self.champ_list[i].fight_group(enemy_list, .9, 10)
            total = 0
            for res in range(len(res_list)):
                if res_list[res] == 0:
                    total += 1
                    self.score[i,enemy_list[res].cid - 1] = 1
                elif res_list[res] == 1:
                    self.score[enemy_list[res].cid - 1, i] = 1
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

