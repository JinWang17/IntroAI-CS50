import csv
import sys
from time import strptime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
# why this indent??

        evidence = []
        labels = []
        for row in reader:
            temp = process(row)
            evidence.append(temp)
            labels.append(1 if row[17] == "TRUE" else 0)
        
    return(evidence, labels)


def process(row):
    """
    - Administrative, an integer
    - Administrative_Duration, a floating point number
    - Informational, an integer
    - Informational_Duration, a floating point number
    - ProductRelated, an integer
    - ProductRelated_Duration, a floating point number
    - BounceRates, a floating point number
    - ExitRates, a floating point number
    - PageValues, a floating point number
    - SpecialDay, a floating point number
    - Month, an index from 0 (January) to 11 (December)
    - OperatingSystems, an integer
    - Browser, an integer
    - Region, an integer
    - TrafficType, an integer
    - VisitorType, an integer 0 (not returning) or 1 (returning)
    - Weekend, an integer 0 (if false) or 1 (if true)
    """
    temp = [float(cell) for cell in row[:9]]
    temp[0] = int(temp[0])
    temp[2] = int(temp[2])
    temp[4] = int(temp[4])
    if row[10] == "June":
        row[10] = "Jun"
    temp.append(strptime(row[10], "%b").tm_mon - 1)
    temp.extend([int(cell) for cell in row[11:14]])
    temp.append(1 if row[15] == "Returning_Visitor" else 0)
    temp.append(1 if row[16] == "TRUE" else 0)
    return(temp)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors = 1) 
    model.fit(evidence, labels)
    return(model)

def evaluate(labels, predictions):
    # y_test, predictions
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct_pos = 0
    correct_neg = 0
    pos = 0
    neg = 0

    for actual, predicted in zip(labels, predictions):
        if predicted == 1:
            pos += 1
            if actual == predicted:
                correct_pos += 1
        else:
            neg += 1
            if actual == predicted:
                correct_neg += 1
    #set_trace()            
    sensitivity = correct_pos / pos
    specificity = correct_neg / neg
    return(sensitivity, specificity)



if __name__ == "__main__":
    main()

