import json
import requests
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def ind():
  return render_template('ind.html')

@app.route('/tt')
def tt():
    

#These are given
    shopify_APIKEY = "//enter ur shop api key " 
    shopify_Password = "//enter ur shop api password"
    SHOP_NAME = "//enter ur shop name"
    API_VERSION = "//enter ur api version"

    #From Shopify API: GET /admin/api/2021-04/orders.json?status=any
    shop_url = "https://%s:%s@%s.myshopify.com/admin/api/%s/orders.json?status=any" % (shopify_APIKEY, shopify_Password,SHOP_NAME, API_VERSION)

    response = requests.get(shop_url)
    json_data = json.loads(response.content)

#print(json_data["orders"][0]["id"])
    to_upload = {}
    for order in json_data["orders"]:
        line_items = []
        cust_items = []
        tag_items = []

        for item in order["line_items"]:
            line_items.append(item["name"])
        to_upload[order["id"]] = line_items
        
        
        cust_items = order["customer"]["last_name"]
        tag_items = order["tags"]
        to_upload[order["id"]] = [line_items,cust_items,tag_items]

    


    URL = "postgres://doslajboilntpo:e55bd2433fac77f5d86037b5d3a27691cc73adf1ba07de17c0c9a91a911c4faa@ec2-54-163-254-204.compute-1.amazonaws.com:5432/de4fue4a8a0q2d"
    conn = psycopg2.connect(URL, sslmode='require')
    cur = conn.cursor()

    for item in to_upload:
    
       
        #postgres_insert_query = "INSERT IGNORE INTO shopify (id,line_items,cust_items,tag_items) VALUES (%s,%s,%s,%s)"
        #qry = "INSERT INTO shopify(id,line_items,cust_items,tag_items) VALUES (%s,%s,%s,%s) WHERE NOT EXISTS ( SELECT id FROM shopify WHERE id = %s)"
        a="INSERT INTO shopify(id,line_items,cust_items,tag_items) VALUES (%s,%s,%s,%s)"
  
        line_items,cust_items,tag_items = to_upload[item] 
        records = (item,line_items,cust_items,tag_items,)
        try:
            cur.execute(a,records)
            conn.commit()
        except:
            pass

    conn.rollback()
        #cur.execute(qry,records)
    #conn.commit()
        #cur.execute(postgres_insert_query,records)                       
    
    
    cur.execute("SELECT * FROM shopify")
    data = cur.fetchall()
    return render_template('tt.html', data=data)

    conn.close()

if __name__ == "__main__":

    app.run(debug=True)

  

