from api.endpoints import NotifyError, AddClient
from bootstrap import app, api

api.add_resource(NotifyError, '/api/v1/notifyError')
api.add_resource(AddClient, '/api/v1/addClient')

if __name__ == '__main__':
    app.run(debug=True, port=80)
