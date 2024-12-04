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

def candidate_elimination(training_data, attributes):
    
    # Initialize S to the most specific hypothesis
    S = [['∅'] * len(attributes)]
    # Initialize G to the most general hypothesis
    G = [['?'] * len(attributes)]
    
    def consistent(example, hypothesis):
        """Check if a hypothesis is consistent with an example."""
        for i in range(len(hypothesis)):
            if hypothesis[i] != '?' and hypothesis[i] != example[i]:
                return False
        return True
    
    def minimal_generalization(hypothesis, example):
        for i in range(len(hypothesis)):
            if hypothesis[i] == '∅':
                hypothesis[i] = example[i]
            elif hypothesis[i] != example[i]:
                hypothesis[i] = '?'
        return hypothesis
    
    def minimal_specializations(hypothesis, example):
        """Specialize a hypothesis minimally to exclude the example."""
        specializations = []
        for i in range(len(hypothesis)):
            if hypothesis[i] == '?':
                for value in attributes[i]:
                    if value != example[i]:
                        specialized_hypothesis = hypothesis.copy()
                        specialized_hypothesis[i] = value
                        specializations.append(specialized_hypothesis)
            elif hypothesis[i] != example[i] and hypothesis[i] != '∅':
                specialized_hypothesis = hypothesis.copy()
                specialized_hypothesis[i] = '∅'
                specializations.append(specialized_hypothesis)
        return specializations
    
    for features, label in training_data:
        if label == 'yes': 
            # Remove inconsistent hypotheses from G
            G = [g for g in G if consistent(features, g)]
            # Generalize S to include the example
            S = [minimal_generalization(s, features) for s in S]
        else: 
            # Remove inconsistent hypotheses from S
            S = [s for s in S if not consistent(features, s)]
            # Specialize G to exclude the example
            G_new = []
            for g in G:
                if consistent(features, g):
                    G_new.extend(minimal_specializations(g, features))
                else:
                    G_new.append(g)
            G = G_new
    
    return S, G


if __name__ == "__main__":

    training_data = load_training_data('training_data.csv')
    
    # Define attributes
    attributes = [
        ['sunny', 'rainy'],  # Weather
        ['warm', 'cold'],    # Temperature
        ['normal', 'high'],  # Humidity
        ['strong', 'weak'],  # Wind
        ['warm', 'cool'],    # Water
        ['same', 'change']   # Forecast
    ]
    
    S, G = candidate_elimination(training_data, attributes)
    
    print("Final Specific Boundary (S):")
    print(S)
    print("\nFinal General Boundary (G):")
    print(G)
