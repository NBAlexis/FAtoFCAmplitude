from FAAmplitudeParser import *

folderName = "F:\\PyworkingFolder\\FAtoFCAmplitude\\_TestFile\\"
fileName = "amp11.txt"
fromFeynCalc = False;

fileObj = open(folderName + fileName, "r")
txtContent = fileObj.read()
lastS = txtContent.rfind(']')
txtContent = txtContent[:lastS] + ',' + txtContent[lastS:]

txtContent = TranslateEpsFirstTime(txtContent, fromFeynCalc)
# print(txtContent)
lstAmplitudes = GetAllAmplitudes(txtContent, fromFeynCalc)
ampliIndex = 1

for amplitude in lstAmplitudes:
    replaced = TranslateRemoveLineBreaker(amplitude)
    replaced = TranslatePolarization(replaced, fromFeynCalc)
    replaced = TranslateConjugate(replaced)
    replaced = TranslateMomentum(replaced, fromFeynCalc)
    replaced = TranslateScalarProduct(replaced, fromFeynCalc)
    replaced = TranslateMatrixTensor(replaced, fromFeynCalc)
    replaced = TranslateParameters(replaced)
    replaced = TranslateDenominator(replaced, fromFeynCalc)
    replaced = TranslateScalarProduct(replaced, fromFeynCalc)
    replaced = TranslateDiracMatrix(replaced, fromFeynCalc)
    replaced = TranslateSpinor(replaced, fromFeynCalc)
    replaced = TranslateLorentzAndMomentumBack(replaced)
    replaced = TranslateCompactSpace(replaced)
    print("Amp" + str(ampliIndex), "=", replaced, ";")
    ampliIndex = ampliIndex + 1
fileObj.close()

