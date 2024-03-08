import random
from mingus.containers import Note, Bar, Composition, Track
from mingus.midi import midi_file_out
import music21 as m21

#文字を数字に
def stum(str_moji:str):
    number = ""
    for i in str_moji:
        number += str(ord(i))
    return int(number)

#数字を文字に
def nust(number:int):
    str_number = str(number)
    number_list =[]
    strmoji = ""
    for i in range(len(str_number)):
        number_pre = ""
        if (i+1)%2 == 0:
            number_pre += str_number[len(str_number)-i-1]
            number_pre += str_number[len(str_number)-i]
            number_list.append(int(number_pre))
        elif ((i+1)%2 == 1) and (i == len(str_number)-1):
            number_pre += str_number[len(str_number)-i-1]
            number_list.append(int(number_pre))
    number_list.reverse()
    for i in list(map(chr,number_list)):
        strmoji += i
    return str(strmoji)

#三つの数字で別の数字に
def rsac(num:int):
    rsa = [random.randrange(1,1000),random.randrange(1,2000),random.randrange(1,3000)]
    num -= rsa[0]
    num *= rsa[1]
    num += rsa[2]
    rsas = ""
    str_num = str(num)
    for i in list(map(str, rsa)):
        if len(i) < 4:
            rsas += "0"*(4-len(i)) + i
        else:
            rsas += i
    str_num += rsas
    str_num = bin(int(str_num)<<3)
    str_num = int(str_num, 2)
    return int(str_num)

#三つの数字で元の数字に
def rsab(num:int):
    num = bin(num>>3)
    num = int(num, 2)
    str_num = str(num)
    rsa = []
    rsas = ""
    for i in range(3):
        rsas = ""
        rsas += str_num[len(str_num)-4-(4*i)]
        rsas += str_num[len(str_num)-3-(4*i)]
        rsas += str_num[len(str_num)-2-(4*i)]
        rsas += str_num[len(str_num)-1-(4*i)]
        rsa.append(int(rsas))
    num = int(str_num[0:len(str_num)-12])
    num -= rsa[0]
    num /= rsa[1]
    num += rsa[2]
    return int(num)

#暗号化
def encryption(moji:str):
    if len(moji)//7 >= 1:
        moji_pre = [moji[i: i+7] for i in range(0, len(moji), 7)]
        return_moji = ""
        for i in range(len(moji_pre)):
            return_moji += str(rsac(stum(moji_pre[i])))
            if i < len(moji_pre)-1:
                return_moji += "&"
        return return_moji
    elif len(moji)//7 <= 0:
        return rsac(stum(moji))
   

#復号
def decryption(num:str):
    if str(num).count("&") <= 0:
        return nust(rsab(int(num)))
    elif str(num).count("&") >= 1:
        num_pre = str(num).split("&")
        return_num = ""
        for i in range(num.count("&")+1):
           return_num += nust(rsab(int(num_pre[i])))
        return return_num

# print(encryption("HELLO WORLD"))
# print(decryption("657768579625240536039290503112&58114074728535207299456"))

#数字から音楽に
def cmusic(num:str,url:str="Doremi.midi"):
    scale = []
    list_num = []
    if num.count("&") >= 1:
        list_num = str(num).split("&")
    elif num.count("&") <= 0:
        list_num.append(str(num))
    for i in list_num:
        for j in i:
            if j == "0":
                scale.append("C-3")
            elif j == "1":
                scale.append("D-3")
            elif j == "2":
                scale.append("E-3")
            elif j == "3":
                scale.append("F-3")
            elif j == "4":
                scale.append("G-3")
            elif j == "5":
                scale.append("A-3")
            elif j == "6":
                scale.append("B-3")
            elif j == "7":
                scale.append("C-4")
            elif j == "8":
                scale.append("D-4")
            elif j == "9":
                scale.append("E-4")
        scale.append("F-4")

    composition = Composition()
    track = Track()
    bar = Bar()
    bar.set_meter((4, 4))
    for note in scale:
        bar + Note(note)
        if bar.is_full():
            track + bar
            bar = Bar()
            bar.set_meter((4, 4))
    if not bar.is_full():
        track + bar
    composition.add_track(track)
    midi_file_out.write_Composition(url, composition)
    
def bmusic(url:str = "Doremi.midi"):
    return_str = ""
    frog = m21.converter.parse(url)
    for measure in frog[1]:
        for item in measure:
            if isinstance(item, m21.note.Note):
                if item.pitches[0].midi  == 48:
                    return_str += "0"
                elif item.pitches[0].midi  == 50:
                    return_str += "1"
                elif item.pitches[0].midi  == 52:
                    return_str += "2"
                elif item.pitches[0].midi  == 53:
                    return_str += "3"
                elif item.pitches[0].midi  == 55:
                    return_str += "4"
                elif item.pitches[0].midi  == 57:
                    return_str += "5"
                elif item.pitches[0].midi  == 59:
                    return_str += "6"
                elif item.pitches[0].midi  == 60:
                    return_str += "7"
                elif item.pitches[0].midi  == 62:
                    return_str += "8"
                elif item.pitches[0].midi  == 64:
                    return_str += "9"
                elif item.pitches[0].midi  == 65:
                    return_str += "&"
                
    return_str = return_str.rstrip("&")
    return return_str

def musicEnryption(mojis:str,url:str = "Doremi.midi"):
    return cmusic(encryption(mojis),url)

def musicDecryption(url:str="Doremi.midi",flag:bool = True):
    return_mojis = decryption(bmusic(url))
    if flag:
        print(return_mojis)
        return return_mojis
    else:
        return return_mojis

musicEnryption("HELLO WORLD")