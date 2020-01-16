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
                        r'PolarizationVector[Momentum[\g<1>], LorentzIndex[mu\g<2>]]', amplitude)
        return retStr
    retStr = re.sub(r'PolarizationVector\[\s*([kp][\d]+)\s*,\s*li([\d]+)\s*\]',
                    r'PolarizationVector[Momentum[\g<1>], LorentzIndex[mu\g<2>]]', amplitude)
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
