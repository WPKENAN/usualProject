function X = normalize(I)

minValue = min(min(I));
maxValue = max(max(I));
X = (I - minValue) /(maxValue - minValue);