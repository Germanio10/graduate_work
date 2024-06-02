import assertion
from config import cfg, logger
from locust import HttpUser, LoadTestShape, constant_pacing, task


class AssistantUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    def on_start(self):
        logger.debug("user started")

    @task
    def send_question(self) -> None:
        transaction = self.send_question.__name__
        body = {"text": "Какой рейтинг у фильма гладиатор"}
        with self.client.post(
            "/api/v1/assistant/", json=body, catch_response=True, name=transaction
        ) as request:
            assertion.check_http_response(transaction, request)

    def on_stop(self):
        logger.debug("user stopped")


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 20, "users": 5, "spawn_rate": 1},
        {"duration": 40, "users": 10, "spawn_rate": 1},
        {"duration": 60, "users": 15, "spawn_rate": 1},
        {"duration": 80, "users": 20, "spawn_rate": 1},
        {"duration": 100, "users": 25, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None
