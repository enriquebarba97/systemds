#-------------------------------------------------------------
#
# Copyright 2020 Graz University of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#-------------------------------------------------------------

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import slicing.slicer as slicer

file_name = 'salary.csv'
dataset = pd.read_csv(file_name)
attributes_amount = len(dataset.values[0])
# for now working with regression datasets, assuming that target attribute is the last one
# currently non-categorical features are not supported and should be binned
y = dataset.iloc[:, attributes_amount - 1:attributes_amount].values
# starting with one not including id field
x = dataset.iloc[:, 1:attributes_amount - 1].values
# list of numerical columns
non_categorical = [4, 5]
for row in x:
    for attribute in non_categorical:
        # <attribute - 2> as we already excluded from x id column
        row[attribute - 2] = int(row[attribute - 2] / 5)
# hot encoding of categorical features
enc = OneHotEncoder(handle_unknown='ignore')
x = enc.fit_transform(x).toarray()
complete_x = []
complete_y = []
counter = 0
for item in x:
    complete_row = (counter, item)
    complete_x.append(complete_row)
    complete_y.append((counter, y[counter]))
    counter = counter + 1
x_size = counter
# train model on a whole dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
model = LinearRegression()
model.fit(x_train, y_train)
f_l2 = sum((model.predict(x_test) - y_test) ** 2)/x_size
# alpha is size significance coefficient
# verbose option is for returning debug info while creating slices and printing it
# k is number of top-slices we want
# w is a weight of error function significance (1 - w) is a size significance propagated into optimization function
slicer.process(enc, model, complete_x, complete_y, f_l2, x_size, x_test, y_test, debug=True, alpha=4, k=10, w=0.5)
