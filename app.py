from flask import Flask
from flask import request

app = Flask(__name__)

seen_strings = {}

@app.route('/')
def root():
    return '''
    <pre>
    Welcome to the Stringinator 3000 for all of your string manipulation needs.

    GET / - You're already here!
    POST /stringinate - Get all of the info you've ever wanted about a string. Takes JSON of the following form: {"input":"your-string-goes-here"}
    GET /stats - Get statistics about all strings the server has seen, including the longest and most popular strings.
    </pre>
    '''.strip()

@app.route('/stringinate', methods=['GET','POST'])
def stringinate():
    input = ''
    if request.method == 'POST':
        input = request.json['input']
    else:
        input = request.args.get('input', '')

    if input in seen_strings:
        seen_strings[input] += 1
    else:
        seen_strings[input] = 1
    s={}
    for i in input:
        s[i]=input.count(i)
    l=s.values()
    test=max(l)
    keys=[k for k,v in s.items() if v == test]
    
    return {
        "input": input,
        "length": len(input),
        "longest_char_found":keys,
        "number_of_occurence":test
    }

@app.route('/stats')
def string_stats():
    list1=list(seen_strings.values())
    max_element=0
    check=0
    if len(list1)>=1:
        check=max(list1)
        keys = [k for k, v in seen_strings.items() if v == check]
        max_element=keys
    list2=list(seen_strings)
    long=0
    if len(list2)>=1:
        long=max(list2,key=len)
    return {
        "inputs": seen_strings,
        "most_popular_key":max_element,
        "longest_input_received":long,
    }

if __name__ == '__main__':
   app.run()