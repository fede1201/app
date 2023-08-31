import datetime
from flask import Flask, request, jsonify
import base64
import io

app = Flask(__name__)

@app.route('/generate_txt', methods=['POST'])
def generate_txt():
    data_list = request.json
    output = io.StringIO()
    
    for data in data_list:
        azienda = data["azienda"]
        target_list = data["target"]
        totale = round(data["totale"], 2)
        
        output.write(f"{azienda['ragioneSociale']:<30} {totale:>10.2f}€\n\n")

        for target in target_list:
            date_str = target['dataFattura'].split(" (")[0]
            date_obj = datetime.datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S GMT%z")
            formatted_date = date_obj.strftime("%d/%m/%Y")
            dare = round(target['dare'], 2)
            output.write(f"{target['numeroFattura']:<15} {formatted_date:<20} {dare:>10.2f}€\n")
        
    # Convertire il buffer in Base64
    base64_txt = base64.b64encode(output.getvalue().encode()).decode('utf-8')
    
    return jsonify({"base64_txt": base64_txt})

if __name__ == '__main__':
    app.run(debug=True)
