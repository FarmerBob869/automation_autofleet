from flask import Flask, jsonify

def create_app(testing=False):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(polygon_blueprint, url_prefix='/polygon')
    app.register_blueprint(metrics_blueprint, url_prefix='/metrics')
    app.register_blueprint(zkevm_blueprint, url_prefix='/zkevm')

 
    })



     @app.route('/health', methods=['GET'])
    def health_check():
        health_status = {
            'mongodb': check_mongodb(),
            'redis': check_redis(),
            'celery': check_celery()
        }
        return jsonify(health_status)