import re


def GetAllAmplitudes(content: str, fromFeynCalc: bool) -> []:
    pattern = re.compile(r'FeynAmp\[[^\]]*\],([\w\W]*?)\],')
    if fromFeynCalc:
        pattern = re.compile(r'FAFeynAmp\[[^\]]*\],([\w\W]*?)\],')
    allMatches = pattern.findall(content)
    return allMatches


def TranslateRemoveLineBreaker(amplitude: str) -> str:
    retStr = re.sub('[\\n\\r]', '', amplitude)
    return retStr


def TranslatePolarization(amplitude: str, fromFeynCalc: bool) -> str:
    if fromFeynCalc:
        retStr = re.sub(r'FAPolarizationVector\[\s*([kp][\d]+)\s*,\s*li([\d]+)\s*\]',
                        r'PolarizationVector[\g<1>, LorentzIndex[mu\g<2>]]', amplitude)
        return retStr
    retStr = re.sub(r'PolarizationVector\[\s*([kp][\d]+)\s*,\s*li([\d]+)\s*\]',
                    r'PolarizationVector[\g<1>, LorentzIndex[mu\g<2>]]', amplitude)
    return retStr


def TranslateConjugate(amplitude: str) -> str:
    retStr = re.sub(r'Conjugate\[', r'ComplexConjugate[', amplitude)
    return retStr


def TranslateMomentum(amplitude: str, fromFeynCalc: bool) -> str:
    if fromFeynCalc:
        retStr = re.sub(r'FAFourVector\[([^,]*?),\s*li([\d]+)\s*\]',
                        r'Pair[Momentum[\g<1>], LorentzIndex[mu\g<2>]]', amplitude)
        return retStr
    retStr = re.sub(r'FourVector\[([^,]*?),\s*li([\d]+)\s*\]',
                    r'Pair[Momentum[\g<1>], LorentzIndex[mu\g<2>]]', amplitude)
    return retStr


def TranslateScalarProduct(amplitude: str, fromFeynCalc: bool) -> str:
    if fromFeynCalc:
        retStr = re.sub(r'FAScalarProduct\[([^,]*?),\s*([^\s]+)\s*\]',
                        r'Pair[Momentum[\g<1>], Momentum[\g<2>]]', amplitude)
        return retStr
    retStr = re.sub(r'ScalarProduct\[([^,]*?),\s*([^\s]+)\s*\]',
                    r'Pair[Momentum[\g<1>], Momentum[\g<2>]]', amplitude)
    return retStr


def TranslateMatrixTensor(amplitude: str, fromFeynCalc: bool) -> str:
    if fromFeynCalc:
        retStr = re.sub(r'FAMetricTensor\[\s*li([\d+])\s*,\s*li([\d+])\s*\]',
                        r'Pair[LorentzIndex[mu\g<1>], LorentzIndex[mu\g<2>]]', amplitude)
        return retStr
    retStr = re.sub(r'MetricTensor\[\s*li([\d+])\s*,\s*li([\d+])\s*\]',
                    r'Pair[LorentzIndex[mu\g<1>], LorentzIndex[mu\g<2>]]', amplitude)
    return retStr


def TranslateParameters(amplitude: str) -> str:
    retStr = re.sub(r'FCGV\[\"([\w\d]+)\"\]',
                    r'\g<1>', amplitude)
    return retStr


def TranslateDenominator(amplitude: str, fromFeynCalc: bool) -> str:
    if fromFeynCalc:
        retStr = re.sub(r'FAPropagatorDenominator\[([^,]+),\s*([^\]]+)\]',
                        r'(1/(Pair[Momentum[\g<1>], Momentum[\g<1>]] - \g<2>^2))', amplitude)
        return retStr
    retStr = re.sub(r'PropagatorDenominator\[([^,]+),\s*([^\]]+)\]',
                    r'(1/(Pair[Momentum[\g<1>], Momentum[\g<1>]] - \g<2>^2))', amplitude)
    return retStr


def TranslateCompactSpace(amplitude: str) -> str:
    retStr = re.sub(r'[\s]+',
                    r' ', amplitude)
    return retStr


def TranslateEpsFirstTime(amplitude: str, fromFeynCalc: bool) -> str:
    """
    To replace LeviCivita to Eps, at the same time remove the ], combination in this function
    :param amplitude:
    :param fromFeynCalc:
    :return:
    """
    if fromFeynCalc:
        print("TranslateEps not supported for FeynCalc yet")
        return amplitude
    retStr: str = amplitude
    iPosition: int = 0
    iPosition = retStr.find("LeviCivita[")
    print("LeviCivita Position: ", iPosition)
    while iPosition >= 0:
        # find the corresponding ]
        level: int = 0
        iPosition2: int = iPosition
        while iPosition2 < len(retStr):
            if retStr[iPosition2] == '[':
                level = level + 1
            if retStr[iPosition2] == ']':
                if level > 1:
                    level = level - 1
                else:
                    toReplace: str = retStr[iPosition:iPosition2+1]
                    replaceStr: str = toReplace
                    replaceStr = re.sub(r'(FourVector)\[([^\]]*?)\]', r'Momentum(\g<2>)', replaceStr)
                    replaceStr = re.sub(r'LeviCivita\[([^,^\]]*),\s*([^,^\]]*)\]', r'Eps[LorentzIndex_\g<1>_, LorentzIndex_\g<2>_]', replaceStr)
                    replaceStr = re.sub(r'LeviCivita\[([^,^\]]*),\s*([^,^\]]*),\s*([^,^\]]*)\]',
                                        r'Eps[LorentzIndex_\g<1>_, LorentzIndex_\g<2>_, LorentzIndex_\g<3>_]', replaceStr)
                    replaceStr = re.sub(r'LeviCivita\[([^,^\]]*),\s*([^,^\]]*),\s*([^,^\]]*),\s*([^,^\]]*)\]',
                                        r'Eps[LorentzIndex_\g<1>_, LorentzIndex_\g<2>_, LorentzIndex_\g<3>_, LorentzIndex_\g<4>_]', replaceStr)
                    replaceStr = re.sub(r'LorentzIndex\_Momentum\(([^\]^\)]+)\)\_', r'Momentum_\g<1>_', replaceStr)
                    retStr = retStr.replace(toReplace, replaceStr)
                    iPosition = retStr.find("LeviCivita[")
                    iPosition2 = len(retStr)
            iPosition2 = iPosition2 + 1
    return retStr


def TranslateScalarProduct(amplitude: str, fromFeynCalc: bool) -> str:
    if fromFeynCalc:
        print("TranslateEps not supported for FeynCalc yet")
        return amplitude
    retStr = re.sub(r'ScalarProduct\[\s*([^\]^\,]+)\s*\,\s*([^\]^\,]+)\s*\]',
                    r'Pair[Momentum_\g<1>_, Momentum_\g<2>_]', amplitude)
    return retStr


def TranslateDiracMatrix(amplitude: str, fromFeynCalc: bool) -> str:
    if fromFeynCalc:
        print("TranslateEps not supported for FeynCalc yet")
        return amplitude
    retStr = re.sub(r'DiracMatrix\[([^\[^\]]+?)\]', r'GA[LorentzIndex[\g<1>]]', amplitude)
    retStr = re.sub(r'DiracSlash\[([^\[^\]]+?)\]', r'GS[Momentum[\g<1>]]', retStr)
    retStr = re.sub(r'ChiralityProjector\[1\]', r'((1+GA5)/2)', retStr)
    retStr = re.sub(r'ChiralityProjector\[-1\]', r'((1-GA5)/2)', retStr)
    return retStr


def TranslateSpinor(amplitude: str, fromFeynCalc: bool) -> str:
    """
    Currently only support initial state
    :param amplitude:
    :param fromFeynCalc:
    :return:
    """
    if fromFeynCalc:
        print("TranslateSpinor not supported for FeynCalc yet")
        return amplitude
    retStr = re.sub(r'DiracSpinor\[\s*-\s*(p[\d]+)\s*,([^\]]+)\]', r'SpinorVBar[Momentum[\g<1>],\g<2>]', amplitude)
    retStr = re.sub(r'DiracSpinor\[\s*(p[\d]+)\s*,\s*([^\]]+)\]', r'SpinorU[Momentum[\g<1>], \g<2>]', retStr)
    return retStr


def TranslateLorentzAndMomentumBack(amplitude: str) -> str:
    retStr = re.sub(r'Momentum\_([^\_]*?)\_', r'Momentum[\g<1>]', amplitude)
    retStr = re.sub(r'LorentzIndex\_([^\_]*?)\_', r'LorentzIndex[\g<1>]', retStr)
    retStr = re.sub(r'li([\d]+)', r'mu\g<1>', retStr)
    return retStr
