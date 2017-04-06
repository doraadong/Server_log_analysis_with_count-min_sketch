class controller:

    def __init__(self, filename, output_folder):
        self.filename = filename
        self.features = []
        self.directory = output_folder

    def register(self, feature):
        self.features.append(feature)

    def run(self):
        
        # setup output path and open each file 
        outputs = []
        for feature in self.features: 
            output_name = self.directory + '/' + feature.__class__.__name__ + '.txt'
            output_file = open(output_name, 'w')
            outputs.append(output_file)
                    
        with open(self.filename,"r",encoding="latin-1") as file:
            for line in file:
                for i in range(len(self.features)):
                    self.features[i].process_line(line, outputs[i])
       
        # print results
        for i in range(len(self.features)):
            self.features[i].print_results(outputs[i])
            
    
        # close output files
        for output in outputs: 
            output.close()