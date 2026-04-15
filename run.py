from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    # Use SocketIO's run which wraps around eventlet/gevent
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
