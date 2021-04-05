import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        # ???????
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            # if person has trait from knowledge but not captured in the have_trait set, 
            # then we know we should skip this probability
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # make sure 1) one_gene and two_gene are exclusive
                # 2) one_gene + two_gene <= names            
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    # return all non-repeated subsets of s 
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    p = 1
    
    # update contribution of probability from gene
    for person in set(people):
        mother = people[person]['mother']
        father = people[person]['father']
        # everyone in set `one_gene` has one copy of the gene
        if person in one_gene: 
            if mother and father:
                p *= compute_child(father, mother, 1, one_gene, two_genes)
            else: 
                p *= PROBS["gene"][1] 
            # update trait
            p *= PROBS["trait"][1][True] if person in have_trait else PROBS["trait"][1][False] 
        # everyone in set `two_genes` has two copies of the gene
        elif person in two_genes:
            if mother and father:
                p *= compute_child(father, mother, 2, one_gene, two_genes)
            else: 
                p *= PROBS["gene"][2] 
            # update trait
            p *= PROBS["trait"][2][True] if person in have_trait else PROBS["trait"][2][False] 
        # everyone not in `one_gene` or `two_gene` does not have the gene
        else:
            if mother and father:
                p *= compute_child(father, mother, 0, one_gene, two_genes)
            else: 
                p *= PROBS["gene"][0] 
            # update trait
            p *= PROBS["trait"][0][True] if person in have_trait else PROBS["trait"][0][False] 
    
    return p
    
      
    
def compute_child(father, mother, n, one_gene, two_genes):
    """
    computes and returns the probability of the child having n copies of genes
    given the name of this person's mother and father
    """
    # the prpbability that father passes 1 or 0 gene to the child
    from_father = {
        "gene": {
            1: 0,
            0: 0
        }
    }   
    if father in two_genes:
        from_father["gene"][1] = 1 - PROBS["mutation"]
        from_father["gene"][0] = PROBS["mutation"]
    elif father in one_gene:
        from_father["gene"][1] = 0.5 # 0.5 * PROB["mutation"] + 0.5 * (1 - PROB["mutation"])
        from_father["gene"][0] = 0.5
    else:
        from_father["gene"][1] = PROBS["mutation"]
        from_father["gene"][0] = 1 - PROBS["mutation"]
    
    # the prpbability that mother passes 1 or 0 gene to the child
    from_mother = {
        "gene": {
            1: 0,
            0: 0
        }
    }   
    if mother in two_genes:
        from_mother["gene"][1] = 1 - PROBS["mutation"]
        from_mother["gene"][0] = PROBS["mutation"]
    elif mother in one_gene:
        from_mother["gene"][1] = 0.5 # 0.5 * PROB["mutation"] + 0.5 * (1 - PROB["mutation"])
        from_mother["gene"][0] = 0.5
    else:
        from_mother["gene"][1] = PROBS["mutation"]
        from_mother["gene"][0] = 1 - PROBS["mutation"]
   
    # probability that child has 0/1/2 genes from parents
    if n == 2:
        return from_father["gene"][1] * from_mother["gene"][1]
    elif n == 1:
        return (from_father["gene"][1] * from_mother["gene"][0] +
         from_mother["gene"][1] * from_father["gene"][0])
    else:
        return from_father["gene"][0] * from_mother["gene"][0]
                                                            



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in set(probabilities):
        # update to gene part
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        
        # update to trait part
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p        
    
    # this function operates on the original copy of probabilities; therefore no need to return
    

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in set(probabilities):
        # normlize gene part
        gene_sum = (probabilities[person]["gene"][1] + probabilities[person]["gene"][2] +
         probabilities[person]["gene"][0])
        probabilities[person]["gene"][1] /= gene_sum
        probabilities[person]["gene"][2] /= gene_sum
        probabilities[person]["gene"][0] /= gene_sum
        
        # normalize trait part
        trait_sum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] /= trait_sum 
        probabilities[person]["trait"][False] /= trait_sum 
        
    # this function operates on the original copy of probabilities; therefore no need to return


if __name__ == "__main__":
    main()

