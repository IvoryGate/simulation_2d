from src.builder.loop import Loop
import time

if __name__ == "__main__":
    config_path = "config.json"
    start_time = time.time()
    Loop().run(config_path=config_path)
    end_time = time.time()
    print(end_time-start_time)