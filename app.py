from flask import Flask, request
from multiprocessing import Value

# init counter variable as shared value
counter = Value('i', 0)
app = Flask(__name__)

@app.route('/counter-service', methods=['GET', 'POST'])
def counter_service():
    
    # handle POST request
    if request.method == 'POST':
        counter.value +=  1
        return ''''''

    # handle GET request
    return '''{}'''.format(counter.value)
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)