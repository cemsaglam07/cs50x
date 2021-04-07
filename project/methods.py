def fafsa(filename):
    with open(filename, "r") as f:
        raw = f.read().splitlines()
    data = {}
    tmp = ""
    for item in raw:
        if len(item) > 0 and item[0] == ">":
            tmp = item[1:]
            data[tmp] = ""
        else:
            data[tmp] += item
    return data


def dna(filename):
    with open(filename, "r") as f:
        string = f.read().splitlines()[0]
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for char in string:
        d[char] += 1
    string = str(d["A"]) + " " + str(d["C"]) + " " + str(d["G"]) + " " + str(d["T"])
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(string)
    return filename[:-5] + "o).txt"


def rna(filename):
    with open(filename, "r") as f:
        string = f.read().splitlines()[0].replace("T", "U")
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(string)
    return filename[:-5] + "o).txt"


def revc(filename):
    with open(filename, "r") as f:
        string = str(f.read())[::-1]
    new = ""
    for char in string:
        if char == "A":
            new += "T"
        elif char == "T":
            new += "A"
        elif char == "C":
            new += "G"
        elif char == "G":
            new += "C"
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(new)
    return filename[:-5] + "o).txt"


def fib(filename):
    with open(filename, "r") as f:
        n_k = f.read().split()
    if len(n_k) == 2:
        a = 1
        b = 1
        for i in range(int(n_k[0]) - 1):
            a, b = b, b + a * int(n_k[1])
        with open(filename[:-5] + "o).txt", "w") as ff:
            ff.write(str(a))
        return filename[:-5] + "o).txt"


def gc(filename):
    with open(filename, "r") as f:
        raw = f.read().splitlines()
    data = {}
    tmp = ""
    for item in raw:
        if len(item) > 0 and item[0] == ">":
            tmp = item
            data[tmp] = ["", ""]
        else:
            data[tmp][0] += item

    for key, value in data.items():
        den = 0
        for char in value[0]:
            if char in ["G", "C"]:
                den += 1
        data[key] = float(den) / len(value[0]) * 100

    with open(filename[:-5] + "o).txt", "w") as ff:
        print(max(data, key=data.get)[1:], file=ff)
        print(data[max(data, key=data.get)], file=ff)

    return filename[:-5] + "o).txt"


def hamm(filename):
    with open(filename, "r") as f:
        raw = f.read().splitlines()
    dh = 0
    for i in range(len(raw[0])):
        if raw[0][i] != raw[1][i]:
            dh += 1
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(str(dh))
    return filename[:-5] + "o).txt"


def iprb(filename):
    with open(filename, "r") as f:
        string = f.split()

    k = float(string[0])
    m = float(string[1])
    n = float(string[2])

    s = k + m + n
    k1 = k / s
    m1k2 = (m * k)
    m1m2 = (0.75 * m * (m-1))
    m1n2 = (0.5 * m * n)
    m1 = (m1k2 + m1m2 + m1n2) / (s * (s-1))
    n1k2 = (n * k)
    n1m2 = (0.5 * n * m)
    n1 = (n1k2 + n1m2) / (s * (s-1))

    with open(filename[:-5] + "o).txt", "w") as ff:
        result = k1 + m1 + n1
        ff.write(str(result))


def prot(filename):
    table = {"UUU": "F", "CUU": "L", "AUU": "I", "GUU": "V", "UUC": "F",
             "CUC": "L", "AUC": "I", "GUC": "V", "UUA": "L", "CUA": "L", "AUA": "I",
             "GUA": "V", "UUG": "L", "CUG": "L", "AUG": "M", "GUG": "V", "UCU": "S",
             "CCU": "P", "ACU": "T", "GCU": "A", "UCC": "S", "CCC": "P", "ACC": "T",
             "GCC": "A", "UCA": "S", "CCA": "P", "ACA": "T", "GCA": "A", "UCG": "S",
             "CCG": "P", "ACG": "T", "GCG": "A", "UAU": "Y", "CAU": "H", "AAU": "N",
             "GAU": "D", "UAC": "Y", "CAC": "H", "AAC": "N", "GAC": "D", "CAA": "Q",
             "AAA": "K", "GAA": "E", "CAG": "Q", "AAG": "K", "GAG": "E", "UGU": "C",
             "CGU": "R", "AGU": "S", "GGU": "G", "UGC": "C", "CGC": "R", "AGC": "S",
             "GGC": "G", "CGA": "R", "AGA": "R", "GGA": "G", "UGG": "W", "CGG": "R",
             "AGG": "R", "GGG": "G", "UGA": "", "UAA": "", "UAG": ""}

    with open(filename, "r") as f:
        string = f.read().splitlines()[0]
    result = ""
    for i in range(0, len(string), 3):
        result += table[string[i:i+3]]
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def subs(filename):
    with open(filename, "r") as f:
        raw = f.read().splitlines()
    with open(filename[:-5] + "o).txt", "w") as ff:
        for i in range(0, len(raw[0]) - len(raw[1]) + 1):
            if raw[0][i:i+len(raw[1])] == raw[1]:
                print(i+1, end=" ", file=ff)
        print(file=ff)
    return filename[:-5] + "o).txt"


def cons(filename):
    def get_motifs():
        with open(filename, "r") as f:
            raw = f.read().splitlines()
        data = {}
        tmp = ""
        for item in raw:
            if len(item) > 0 and item[0] == ">":
                tmp = item
                data[tmp] = ""
            else:
                data[tmp] += item
        return list(data.values())

    def raw_profile(motifs):
        data = {}
        k = len(motifs[0])
        for symbol in "ACGT":
            data[symbol] = []
            for j in range(k):
                data[symbol].append(0)
        t = len(motifs)
        for i in range(t):
            for j in range(k):
                symbol = motifs[i][j]
                data[symbol][j] += 1
        return data

    def consensus(motifs):
        k = len(motifs[0])
        p = raw_profile(motifs)
        string = ""
        for j in range(k):
            m = 0
            frequentsymbol = ""
            for symbol in "ACGT":
                if p[symbol][j] > m:
                    m = p[symbol][j]
                    frequentsymbol = symbol
            string += frequentsymbol
        return string

    def profile(motifs):
        motifs = raw_profile(motifs)
        key_list = list(motifs.keys())
        for i in [{k: motifs[k]} for k in key_list]:
            string = repr(i)
            string = string.replace("{", "")
            string = string.replace("}", "")
            string = string.replace("'", "")
            string = string.replace(",", "")
            string = string.replace("[", "")
            string = string.replace("]", "")
            with open(filename[:-5] + "o).txt", "a+") as fff:
                print(string, file=fff)

    motifs = get_motifs()
    with open(filename[:-5] + "o).txt", "w") as ff:
        print(consensus(motifs), file=ff)
    profile(motifs)
    return (filename[:-5] + "o).txt")


def fibd(filename):
    with open(filename, "r") as f:
        raw = f.read().split()
    n = raw[0]
    m = raw[1]
    k = 1

    data = [[0] * m] * n
    data[0] = [1] + data[0][1:]
    for i in range(1, n):
        data[i] = [k * sum(data[i - 1][1:m])] + data[i - 1][0:(m-1)]
    result = sum(data[n - 1])

    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def grph(filename):
    data = fafsa(filename)
    with open(filename[:-5] + "o).txt", "w") as ff:
        for s in data.keys():
            for t in data.keys():
                if data[s][-3:] == data[t][:3] and s != t:
                    print(s + " " + t, file=ff)
    return filename[:-5] + "o).txt"


def iev(filename):
    p = [1.0, 1.0, 1.0, 0.75, 0.5, 0.0]

    with open(filename, "r") as f:
        raw = f.read().split()

    c = 2
    result = 0
    for i, n in enumerate(raw):
        result += (c * int(n) * p[i])

    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def lcsm(filename):
    data = list(fafsa(filename).values())
    s = min(data, key=len)
    c = [s[i: j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]
    c.sort(key=len, reverse=True)
    with open(filename[:-5] + "o).txt", "w") as ff:
        for sub in c:
            t = []
            for item in data:
                if item == s:
                    continue
                t.append(item.find(sub))
            if int(-1) not in t:
                print(sub, file=ff)
                break
    return filename[:-5] + "o).txt"


def mrna(filename):
    table = {"F": 2, "L": 6, "S": 6, "Y": 2, "C": 2, "W": 1, "P": 4, "H": 2,
             "Q": 2, "R": 6, "I": 3, "M": 1, "T": 4, "N": 2, "K": 2, "V": 4,
             "A": 4, "D": 2, "E": 2, "G": 4, "Stop": 3}

    with open(filename, "r") as f:
        string = f.read().splitlines()[0]

    result = 3
    for i in range(len(string)):
        result *= table[string[i]]

    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(str(result % 1000000))
    return filename[:-5] + "o).txt"


def perm(filename):
    import itertools
    with open(filename, "r") as f:
        string = f.read().splitlines()[0]
    perm = list(itertools.permutations([i + 1 for i in range(int(string))]))
    result = str(len(perm))
    for i in range(len(perm)):
        tmp = "\n"
        for j in range(len(perm[i])):
            tmp += str(perm[i][j]) + " "
        result += tmp[:-1:]
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def prtm(filename):
    mass = {"A": 71.03711, "C": 103.00919, "D": 115.02694, "E": 129.04259, "F": 147.06841,
            "G": 57.02146, "H": 137.05891, "I": 113.08406, "K": 128.09496, "L": 113.08406,
            "M": 131.04049, "N": 114.04293, "P": 97.05276, "Q": 128.05858, "R": 156.10111,
            "S": 87.03203, "T": 101.04768, "V": 99.06841, "W": 186.07931, "Y": 163.06333}
    with open(filename, "r") as ff:
        string = ff.read().splitlines()[0]
    with open(filename[:-5] + "o).txt", "w") as f:
        f.write(str(sum([mass[c] for c in string])))
    return filename[:-5] + "o).txt"


def revp(filename):
    def revc_revp(x):
        string = str(x)[::-1]
        new = ""
        for char in string:
            if char == "A":
                new += "T"
            elif char == "T":
                new += "A"
            elif char == "C":
                new += "G"
            elif char == "G":
                new += "C"
        return new

    result = ""
    for key in fafsa(filename).values():
        for i in range(len(key)):
            for j in range(i + 1, len(key) + 1):
                if len(key[i:j]) in range(4, 13):
                    if key[i: j] == revc_revp(key[i: j]):
                        result += str(i + 1) + " " + str(j - i) + "\n"

    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result.rstrip())
    return filename[:-5] + "o).txt"


def splc(filename):
    table = {"UUU": "F", "CUU": "L", "AUU": "I", "GUU": "V", "UUC": "F",
             "CUC": "L", "AUC": "I", "GUC": "V", "UUA": "L", "CUA": "L", "AUA": "I",
             "GUA": "V", "UUG": "L", "CUG": "L", "AUG": "M", "GUG": "V", "UCU": "S",
             "CCU": "P", "ACU": "T", "GCU": "A", "UCC": "S", "CCC": "P", "ACC": "T",
             "GCC": "A", "UCA": "S", "CCA": "P", "ACA": "T", "GCA": "A", "UCG": "S",
             "CCG": "P", "ACG": "T", "GCG": "A", "UAU": "Y", "CAU": "H", "AAU": "N",
             "GAU": "D", "UAC": "Y", "CAC": "H", "AAC": "N", "GAC": "D", "CAA": "Q",
             "AAA": "K", "GAA": "E", "CAG": "Q", "AAG": "K", "GAG": "E", "UGU": "C",
             "CGU": "R", "AGU": "S", "GGU": "G", "UGC": "C", "CGC": "R", "AGC": "S",
             "GGC": "G", "CGA": "R", "AGA": "R", "GGA": "G", "UGG": "W", "CGG": "R",
             "AGG": "R", "GGG": "G", "UGA": "", "UAA": "", "UAG": ""}

    string = max(fafsa(filename).values(), key=len)
    subs = [i for i in fafsa(filename).values() if i != string]
    for i in range(len(subs)):
        string = string.replace(subs[i], "")

    string = string.replace("T", "U")
    result = ""
    for i in range(0, len(string), 3):
        result += table[string[i:i + 3]]

    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def lexf(filename):
    import itertools
    with open(filename, "r") as f:
        data = f.read().splitlines()
    cart = itertools.product(*[data[0].split() for i in range(int(data[1]))])
    result = "\n".join(["".join(i) for i in cart])
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def pmch(filename):
    import math
    d = list(fafsa(filename).values())[0]
    result = math.factorial(d.count("A")) * math.factorial(d.count("G"))
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def pper(filename):
    import math
    with open(filename, "r") as f:
        d = ff.read().split()
        n, k = int(d[0]), int(d[1])
    result = int((math.factorial(n) / (math.factorial(n - k))) % 1000000)
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def sign(filename):
    import itertools
    with open(filename, "r") as f:
        x = list(itertools.permutations(range(1, int(f.read())+1)))
        ll = len(x[0])

    s1 = [str(bin(i))[2:].replace("0", "-").replace("1", "+") for i in range(2 ** ll)]
    s2 = ["-" * (ll - len(c)) + c for c in s1]
    r = ""
    lc = 0
    for t in x:
        for s in s2:
            r += "\n" + " ".join([s[i] + str(t[i]) for i in range(len(s))]).replace("+", "")
            lc += 1
    result = str(lc) + r
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(result)
    return filename[:-5] + "o).txt"


def tran(filename):
    s = list(fafsa(filename).values())
    s1, s2, rn, rd = s[0], s[1], 0, 0
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            continue
        elif s1[i] + s2[i] in ["AG", "GA", "CT", "TC"]:
            rn += 1
        else:
            rd += 1
    with open(filename[:-5] + "o).txt", "w") as ff:
        ff.write(str(rn / rd))
    return filename[:-5] + "o).txt"
