import pandas as pd
from flask import Flask,jsonify
from flask_cors import CORS


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


#Teknisk oppgave i forkant av Finn Intervju
def getData():
    pederArray=[]
    with open('Ads_4.txt','r') as data:
        for line in data:
            corrected = line.strip('\n')
            #currentline contains all the data listed in each line, such that it is possible to loop through.
            currentline= corrected.split(",")
            pederArray.append(currentline)

    df = pd.DataFrame(pederArray, columns =['adID', 'adType','adPrice'])
    print(len(df))

    df = df.astype({"adID": int, "adType": 'category',"adPrice":float })


    adTypeArray=[]

    for i in pederArray:
        if i[1] not in adTypeArray:
            adTypeArray.append(i[1])

    final_array=[]
    final_dict=[]
    for i in adTypeArray:
        all_instances = df.loc[df['adType'] == i]
        #print(all_instances)
        number_of_instances = len(df.loc[df['adType'] == i])
        max_price = "%.2f" % float(all_instances['adPrice'].max())
        min_price = "%.2f" % float(all_instances['adPrice'].min())
        diff = float(max_price)-float(min_price)
        id_max = all_instances['adPrice'].idxmax()
        id_min = all_instances['adPrice'].idxmin()
        test = ["Ad type:"+str(i),"Number of instances: "+str(number_of_instances),"id max: "+str(id_max),"Max Price: "+str(max_price),"ID min: "+str(id_min),"Min Price: "+str(min_price),"Diff: "+str(diff)]
        object ={'type':str(i),'#instances':str(number_of_instances),'highest_id':str(id_max),'highest_amount':str(max_price),'lowest_id':str(id_min),'lowest_amount':str(min_price),'diff':str(diff) }
        temparray=[str(i),str(number_of_instances),str(id_max),float(max_price),str(id_min),float(min_price),float(diff)]
        #print(object)
        final_array.append(temparray)
        final_dict.append(test)
        #print(final_output)
    final_output=[final_array,final_dict]
    return final_output


@app.route('/', methods=['GET'])
def hello():
    data = getData()
    print("DATAAA", data)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
    #host='0.0.0.0', port=8000
