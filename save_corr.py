import sqlite3
import pickle
import csv
import pandas
import math
conn = sqlite3.connect("top1000.db")
c= conn.cursor()
avg_ratings = pickle.load(open("float_avg_user_rating","rb"))

def getCorrelation(user_i="",user_j=""):

    c.execute("SELECT A.movie_id , A.user_id, B.user_id, A.time, B.time, A.review, B.review from (select * from reviews where user_id="+str(user_i)+") as A join (select * from reviews where user_id="+str(user_j)+") as B on A.movie_id=B.movie_id")
    all_results = c.fetchall()
    #print all_results
    mu_i = avg_ratings[int(user_i)]
    mu_j = avg_ratings[int(user_j)]
    M = len(all_results)
    sigma_i =0
    sigma_j = 0
    E = 0
    for row in all_results:
      del_t = -abs(row[3]-row[4])
      E += (row[5] - mu_i) * (row[6] - mu_j)*math.exp(del_t/4959393420)
      sigma_i += math.pow((row[5] - mu_i),2)
      sigma_j += math.pow((row[6] - mu_j),2)
    E/=M
    sigma_i/=M
    sigma_j/=M
    sigma_i = math.sqrt(sigma_i)
    sigma_j = math.sqrt(sigma_j)
    temp = sigma_i*sigma_j
    if temp == 0:
        return 0.9999
    else:
        return E/temp
        correlation = E/(sigma_i*sigma_j)
    # beta = 495
    # gamma = -2.47
    #correlation += gamma
    return correlation






def saveAllCorrelation():
    with open("top_1000_users","rb") as f:
        all_users = pickle.load(f)
    file = open("allCorrelationsFrom519.csv","a+b")
    writer = csv.writer(file)
    user=[]
    for i in range(len(all_users)):
        user.append(list(all_users[i])[0])

    for i in range(531,len(user)):
        for j in range(i + 1,len(user)):
            #print user[i],list(all_users[j])[0]
            print i,j
            corr = getCorrelation(user[i],user[j])
            writer.writerow([i,user[i],user[j],corr])


    file.close()


# def csvToDict():
#     my_dict = {}
#     with open("test_data.csv","rb") as file:
#         reader = pandas.read_csv(file)

#     for i in range(len(reader)):
#         my_dict[str(row[0][i]) +"-"+ str(row[1][i])] = row[2][i]
#     pickle.dump(my_dict,open("allCorrelations","wb")

saveAllCorrelation()
conn.close()
