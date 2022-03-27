

def model_mock(features):
    import time
    time.sleep(2)
    return sum(features) % 10
