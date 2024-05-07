############################################################
# CISC3140- P3
# Due May 6th 11:59 Pm
#
################################################################





################################################################################################
#Function to compute the prior count of Label(L): Nursery admission recommendation
#Input: trainFile - train_data.dat
#Returns: priorCountsList- the number of counts for the two classes {recommend, not-recom}
#
################################################################################################
def getPriorCount(trainFile):
    # Initialize the counts for recommend, not_recom as dictionary (easy/fast access)
    priorCountsList = {"recommend": 0, "not_recom": 0} 
    trainFileObj = open(trainFile,'r')
    trainFileLines=trainFileObj.readlines()
    # Totals the number of times recommend and not_recom appear in the samples
    for trainFileLine in trainFileLines:
        match trainFileLine.strip().split(",")[-1]:
            case "recommend":
                priorCountsList["recommend"] += 1
            case "not_recom":
                priorCountsList["not_recom"] += 1
    trainFileObj.close()
    return priorCountsList


################################################################################################
# Function to compute the CPT for each feature: P(O|L) P(N|L) P(F|L) P(C|L) P(H|L) P(I|L) P(S|L) P(A|L)
#                                              Parents occupation (O): {usual, pretentious, great_pret}
#                                              Childs Nursery (N): {proper, less_proper, improper, critical, very_crit}
#                                              Family form (F): {complete, completed, incomplete, foster}
#                                              Number of children (C): {1, 2, 3, more}
#                                              Housing (H): {convenient, less_conv, critical}
#                                              Finance (I): {convenient, inconv}
#                                              Social (S): {non-prob, slightly_prob, problematic}
#                                              Health (A): {recommended, priority, not_recom}
# Inputs: trainFile-train_data.dat, 
#         priorCountList - the number of samples for different label values , 
#         feature_name - This is used to identify which feature the CPT is computed for. 
#                        It can take one of the following values:occupation, nursery, family_form, children, housing, finance, social, health  
# Returns: feature_cpt - The CPT for feature given in feature_name
#
################################################################################################
def getFeatureCPT(trainFile,feature_name,priorCountsList):
    # Initializes feature_cpt with reccomend and not_recom dictionaries
    feature_cpt = {"recommend": {}, "not_recom": {}}
    # I couldn't think of a better way to initialize the feature values
    # So I made a dictionary of feature names with their respective values
    # And depending on the feature_name param, iterated through its corresponding
    # List of feature values and initialized them to 0 
    feature_dict = {"occupation": ["usual", "pretentious", "great_pret"],
                    "nursery": ["proper", "less_proper", "improper", "critical", "very_crit"],
                    "family_form": ["complete", "completed", "incomplete", "foster"],
                    "children": ["1", "2", "3", "more"],
                    "housing": ["convenient", "less_conv", "critical"],
                    "finance": ["convenient", "inconv"],
                    "social": ["nonprob", "slightly_prob", "problematic"],
                    "health": ["recommended", "priority", "not_recom"]}
    for feature in feature_dict[feature_name]:
        feature_cpt["recommend"].update({feature: 0})
        feature_cpt["not_recom"].update({feature: 0})
    
    # Get index of feature in order to reference feature value in trainFile
    match feature_name:
        case "occupation":
            index = 0
        case "nursery":
            index = 1
        case "family_form":
            index = 2
        case "children":
            index = 3
        case "housing":
            index = 4
        case "finance":
            index = 5
        case "social":
            index = 6
        case "health":
            index = 7

    trainFileObj=open(trainFile,'r')
    trainFileLines=trainFileObj.readlines()
    # Totals the number of times the feature_value appeared in a 
    # Sample with the value of L (recommended or not_recom)
    for trainFileLine in trainFileLines:
        trainFileLine = trainFileLine.strip().split(",")
        feature_value = trainFileLine[index]
        feature_cpt[trainFileLine[-1]][feature_value] += 1

    # Divide every feature_value by the value of L (recommend or not_recom depending on the sample it appeared in)
    # We do this since we have a reduced sample space. This gives us P(feature|L), which is what we want!
    for feature_value in feature_cpt["recommend"]:
        feature_cpt["recommend"][feature_value] /= priorCountsList["recommend"]
        
    for feature_value in feature_cpt["not_recom"]:
        feature_cpt["not_recom"][feature_value] /= priorCountsList["not_recom"]
    
    trainFileObj.close()
    return feature_cpt

################################################################################################
# Function to predict the labels for the samples in the validation file
#   The label is predicted as max( P(L|O,N, F, C, H, I, S, A)) = max(P(O|L) P(N|L) P(F|L) P(C|L) P(H|L) P(I|L) P(S|L) P(A|L) P(L)) 
#                           That is you will treat the label with maximum probability as the prediction from the above formulation
# Inputs: valFile - val_data.dat
#         priorProb - Prior for the label, Nursery admission recommendation
# Returns: predictions - the predicted label for each sample in valFile
#
################################################################################################
def getPredictions(valFile, priorProb, feature1CPT,feature2CPT,feature3CPT,feature4CPT,feature5CPT,feature6CPT,feature7CPT,feature8CPT):
    predictions = []
    valFileObj = open(valFile,'r')
    valFileLines = valFileObj.readlines()
    for valFileLine in valFileLines:
        feature = valFileLine.strip().split(",")

        # Calculate probability of recommend
        recommend_probability = feature1CPT["recommend"][feature[0]] * feature2CPT["recommend"][feature[1]] *\
                                feature3CPT["recommend"][feature[2]] * feature4CPT["recommend"][feature[3]] *\
                                feature5CPT["recommend"][feature[4]] * feature6CPT["recommend"][feature[5]] *\
                                feature7CPT["recommend"][feature[6]] * feature8CPT["recommend"][feature[7]] *\
                                priorProb["recommend"]

        # Calculate probability of not_recom
        not_recom_probability = feature1CPT["not_recom"][feature[0]] * feature2CPT["not_recom"][feature[1]] *\
                                feature3CPT["not_recom"][feature[2]] * feature4CPT["not_recom"][feature[3]] *\
                                feature5CPT["not_recom"][feature[4]] * feature6CPT["not_recom"][feature[5]] *\
                                feature7CPT["not_recom"][feature[6]] * feature8CPT["not_recom"][feature[7]] *\
                                priorProb["not_recom"]
        
        # Append greater probability to predictions list (since that is what is predicted based on the data)
        if recommend_probability > not_recom_probability:
            predictions.append("recommend")
        else:
            predictions.append("not_recom")

    return predictions


if __name__=="__main__":
    trainFile = "train_data.dat"
    valFile = "val_data.dat"
    priorCountsList = getPriorCount(trainFile)
    # Assigns key:value pair as (recommend or not_recom):(amount of (recommend or not_recom) / total amount) 
    priorProb = {label: amount / sum(priorCountsList.values()) for label, amount in priorCountsList.items()}

    occupationCPT = getFeatureCPT(trainFile,"occupation",priorCountsList)
    nusreryCPT = getFeatureCPT(trainFile,"nursery",priorCountsList)
    familyFormCPT = getFeatureCPT(trainFile,"family_form",priorCountsList)
    childrenCPT = getFeatureCPT(trainFile,"children",priorCountsList)
    housingCPT = getFeatureCPT(trainFile,"housing",priorCountsList)
    financeCPT = getFeatureCPT(trainFile,"finance",priorCountsList)
    socialCPT = getFeatureCPT(trainFile,"social",priorCountsList)
    healthCPT = getFeatureCPT(trainFile,"health",priorCountsList)
    lineCounter = 0
    correctCount = 0
    totalCount = 0
    predicList = getPredictions(valFile, priorProb, occupationCPT, nusreryCPT, familyFormCPT, childrenCPT, housingCPT, financeCPT, socialCPT, healthCPT)
    valFileObj = open(valFile,'r')
    valFileLines = valFileObj.readlines()
    for valFileLine in valFileLines:
        label = valFileLine.strip('\n').split(',')[-1]
        if label == predicList[lineCounter]:
            correctCount += 1
        totalCount += 1
        lineCounter += 1
    print("The accuracy of the current predictions is {}".format((correctCount/totalCount)*100))
