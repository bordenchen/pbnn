# Project Title
Using back propagation neural network to predict River dust
## Gettign Started
These instructions will guild you how to deploy the project on a live system
### Prerequisites
python3.6 <br />
numpy library <br />
pandas library <br />
matplotlib library <br />
glob library <br />
### How to Use
download preprocessing directory<br />
using aqi_hourly_data.py to translate epa API open data into proper format.<br />
using aqi_data_normalize.py to normalize to data.<br />
using select_input_item.py to select the item that will be used to train BPNN.<br />
using random_select_df.py randomly select training data and save as a csv file.<br />
<br />
download bpnn directory <br />
using csv file generate by random_select_df.py as aqi_hourly_bpnn.py's training file.

