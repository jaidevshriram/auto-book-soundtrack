class Result:
    def __init__(self, time, result):
        self.time = time
        self.result = result
        
    def __str__(self):
        out = f"{self.time}s found {len(self.result['matches'])} results"
        if len(self.result['matches']):
            main_result = self.result['track']['title']
            out += f" song name {main_result}"
        return out