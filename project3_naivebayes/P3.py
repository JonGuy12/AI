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
    priorCountsList=None
    trainFileObj=open(trainFile,'r')
    trainFileLines=trainFileObj.readlines()
    for trainFileLine in trainFileLines:
        trainFileLine # The line is to makes sure that the code executes without error
        #Write your code here
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
def getFeatureCPT(trainFile,priorCountsList,feature_name):
    feature_cpt=None
    trainFileObj=open(trainFile,'r')
    trainFileLines=trainFileObj.readlines()
    for trainFileLine in trainFileLines:
        trainFileLine # The line is to makes sure that the code executes without error
        #Write your code here
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
    predictions=None
    # Write code here
    
    return predictions


if __name__=="__main__":
    trainFile= "train_data.dat"
    valFile="val_data.dat"
    priorCountsList=getPriorCount(trainFile)
    priorProb=None
    #Write code to compute the priorPob from the priorCountsList and assign it to PriorProb
    #You will pass the computed priorProb to getPredictions
    occupationCPT=getFeatureCPT(trainFile,"occupation",priorCountsList)
    nusreryCPT=getFeatureCPT(trainFile,"nursery",priorCountsList)
    familyFormCPT=getFeatureCPT(trainFile,"family_form",priorCountsList)
    childrenCPT=getFeatureCPT(trainFile,"children",priorCountsList)
    housingCPT=getFeatureCPT(trainFile,"housing",priorCountsList)
    financeCPT=getFeatureCPT(trainFile,"finance",priorCountsList)
    socialCPT=getFeatureCPT(trainFile,"social",priorCountsList)
    healthCPT=getFeatureCPT(trainFile,"health",priorCountsList)
    lineCounter=0
    correctCount=0
    totalCount=0
    predicList=getPredictions(valFile, priorProb, occupationCPT, nusreryCPT, familyFormCPT, childrenCPT, housingCPT, financeCPT, socialCPT, healthCPT)
    valFileObj=open(valFile,'r')
    valFileLines=valFileObj.readlines()
    for valFileLine in valFileLines:
        label=valFileLine.strip('\n').split(',')[-1]
        if label==predicList[lineCounter]:
            correctCount+=1
        totalCount+=1
        lineCounter+=1
    print("The accuracy of the current predictions is {}".format((correctCount/totalCount)*100))
