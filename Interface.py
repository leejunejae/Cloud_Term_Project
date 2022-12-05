from flask import Flask,render_template
#import ListInstance
#import AvailableZone
#import StartInstance
#import AvailableRegions
#import StopInstance
#import CreateInstance
#import RebootInstance
#import ListImages

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()