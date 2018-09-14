from app import app
import os

if __name__ == '__main__':
    port = os.getenv('VCAP_APP_PORT', '8080')

    print('Running On Port: ' + str(port))
    app.run(debug=True, host='0.0.0.0', port=port)