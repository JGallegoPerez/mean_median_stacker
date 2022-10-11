# mean_median_stacker
### A Python module that implements mean and binapprox median stacking for astronomical images

In this respository, I am publishing some of my Python code inspired by the online course **Data-driven Astronomy**, by The University of Sydney, which can be found on Coursera: 
https://www.coursera.org/learn/data-driven-astronomy/home/info

**Image stacking** is a common techique in astronomy to increase the signal-to-noise ratio of astronomical images. Typically, many individual images (*subframes*) are taken of the same target, which are subsequently stacked together to obtain a less noisy, final image. This is a crucial step in astronomical image processing, given that these images tend to be extremely faint and noisy, in contrast to the daytime images most people are used to. 

There is a number of algorithms that have been proposed for stacking. The simplest one we could consider is **mean stacking**, which implies simply obtaining the average value for each pixel. A downside of this method is that the presence of extreme outliers would cause some stacked pixels to deviate to what we might consider more representative values. An alternative is to use the **median**, instead the mean, to calculate central, representative values for each pixel. However, a calculation of the true median implies a great computer memory usage, which can easily overwhelm personal computers and even supercomputers for scientific use. Algorithms have been designed to approximate the value of the true median, thus reducing the memory usage, such as the **binapprox algorithm**:
https://www.stat.cmu.edu/~ryantibs/papers/median.pdf

There are two Python modules in this repository. *stacking.py* contains the methods to perform mean and binapprox median stacking on FITS or TIFF image files. Also, a *demo.py* module is included, running a demonstration with some astronomical images I obtained on my own. The results look as follows:

![mean_saturn](https://user-images.githubusercontent.com/89183135/194998296-0bb4be72-27db-4e4d-88dd-221591c97ad4.png)
*Mean stacking of Saturn, from TIFF image files.*

![binapprox_m33](https://user-images.githubusercontent.com/89183135/194998513-f0de6c9c-5f86-47b9-aab0-78b21697a422.png)
*Binapprox stacking of the core of Triangulum Galaxy, M33, from FITS images. The image appears blurry because the subframes were dithered (slightly moved between subframes), which is common practice when capturing astronomical images. Hopefully though, this will serve as proof of concept.*  


