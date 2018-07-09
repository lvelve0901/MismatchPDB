# Class function containing base-pair data
class NA_JSON:
    def __init__(self):
        # JSON file
        self.json_file = None

        # Index of JSON file contents
        self.indices = []

    def set_json(self, json_file):
        self.json_file = json_file

    # Initialize index to self if self.json_file exists
    def read_idx(self):
        if self.json_file is not None:
            # Make sure indices are strings
            self.indices = [str(i) for i in self.json_file]

        else:
            print "Internal JSON file does not exist."
