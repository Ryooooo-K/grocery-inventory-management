import azure.functions as func

from src.agent_func import bp

app = func.FunctionApp()

app.register_blueprint(bp)
