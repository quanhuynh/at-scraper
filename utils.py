BRANDS = ["hoyt", "pse", "mathews", "bowtech", "pearson", "darton", "athens", "martin", "elite", "xpedition", "obsession"]
COLORS = ["red", "cardinal", "black", "green", "white", "purple", "titanium", "silver", "orange"]
PRICES = [float(x) for x in (200, 1800)]

def _drawLengthsRange():
	return [str(float(x)) for x in range(22, 33)] + [str(x+0.5) for x in range(22, 33)]

def _drawWeightsRange():
	pairs = [("30", "40"), ("35", "45"), ("40", "50"), ("45", "55"), ("50", "60"), ("55", "65"), ("60", "70")]
	weights = set()
	for l,h in pairs:
		weights.add(l+"/"+h)
		weights.add(l+"-"+h)
		weights.add(l)
		weights.add(h)
	return weights


DRAWLENGTHS = _drawLengthsRange()
DRAWWEIGHTS = _drawWeightsRange()