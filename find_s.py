import csv

def load_training_data(file_path):
    training_data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            features = row[:-1]  
            label = row[-1]    
            training_data.append((features, label))
    return training_data

def find_s_algorithm(training_data):

    # Initialize the hypothesis with the first positive example
    hypothesis = None

    for features, label in training_data:
        if label == 'yes':  
            if hypothesis is None:
                hypothesis = features.copy()  # Set the initial hypothesis
            else:
                # Generalize the hypothesis to match this positive example
                for i in range(len(hypothesis)):
                    if hypothesis[i] != features[i]:
                        hypothesis[i] = '?'  # Replace differing attributes with '?'
    
    return hypothesis


if __name__ == "__main__":
    
    training_data = load_training_data('training_data.csv')
    
    hypothesis = find_s_algorithm(training_data)
    
    print(hypothesis)
