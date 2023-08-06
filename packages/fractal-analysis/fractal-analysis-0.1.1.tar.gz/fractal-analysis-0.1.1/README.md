# Fractal Analysis
Fractal and multifractal methods, including

- fractional Brownian motion (FBM) tester
- multifractional Brownian motion (MBM) tester

## To install
To get started, simply do:
```
pip install fractal-analysis
```
or check out the code from out GitHub repository.

You can now use the package in Python with:
```
from fractal_analysis import tester
```

## Examples
Import:
```
from fractal_analysis.tester.series_tester import SeriesTester
```
To test a series ```series```:
```
tester = SeriesTester(x=series)
```

To test if the series is FBM with holder exponent 0.3 and use auto estimated sigma square:

```
is_fbm, sig2, h = tester.is_fbm(h=0.3, sig2=None)
```
If the output contains, for example:
> Bad auto sigma square calculated with error 6.239236333681868. Suggest to give sigma square and rerun.

The auto sigma square estimated is not accurate. One may want to manually choose a sigma square and rerun. For example:
```
is_fbm, sig2, h = tester.is_fbm(h=0.3, sig2=1)
```
One can also test the series without specified holder exponent through either setting ```None``` to ```h``` that searches the correct holder exponent from 0.1 to 1 with step 0.1, or entering customized values. I.e.,
```
is_fbm, sig2, h = tester.is_fbm(h=None, sig2=None)
```
or
```
is_fbm, sig2, h = tester.is_fbm(h=[0,1, 0.2, 0.3], sig2=None)
```
To test if the series is MBM with a given holdr exponent series ```h_mbm``` and use auto estimated sigma square:
```
ret, sig2 = tester.is_mbm(h=h_mbm, sig2=None)
```
If the following appears:
>Bad estimated sigma square: 0.0. Suggest to give sigma square and rerun.

One may want to manually choose a sigma square and rerun. For example:
```
ret, sig2 = tester.is_mbm(h=h_mbm, sig2=1)
```
