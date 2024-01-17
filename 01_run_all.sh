#!/bin/bash -e
# The MIT License (MIT)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, provided that the following conditions are met:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#**The software is provided for research purposes only and may not be used for commercial purposes.**
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


stage=1

head=original  # original or xent
normtype=norm  # max or norm


if [ $stage -le 1 ]; then
  ./02_data_preparation.sh $head $normtype
fi

if [ $stage -le 2 ]; then
  ./03_compute.sh $head $normtype
fi
