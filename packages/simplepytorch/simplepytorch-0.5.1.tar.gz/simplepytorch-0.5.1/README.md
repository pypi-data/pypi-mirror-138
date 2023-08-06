Configure and train deep feedforward PyTorch models with a lot of the
details already or partially implemented.

**DISCLAIMER:** This repo is used for my research.
New versions are not necessarily backwards compatible.  The API is
subject to change at a moment's notice.  If you happen to use it in your
research or work, make sure in your requirements.txt to pin the version
or reference the specific commit you used so you don't suffer unwanted
surprises.

Install
===

```
pip install --upgrade simplepytorch
```


Try an example
===

Download and extract DRIVE dataset to ./data/DRIVE

```
 $ ls data/DRIVE 
test  test.zip  training  training.zip
```

Run an experiment, and give it a name.
```
$ python bin/simple_example.py  test_experiment_1

$ ls results/test_experiment_1
checkpoints  log  perf.csv
```

Look at learning curves (note: demo only runs for 2 epochs)
```
simplepytorch_plot test_experiment  -c "dice|loss"
```

Run demo, with (customizable) guarantees that code completes exactly once and
distributes jobs across GPUs.  (note: uses Redis database to temporarily
monitor current jobs).

```
./bin/example_experiments.sh
```



**NOTE:** The readme below this point is very out-dated.  I no longer
use the FeedForward class.


Quick Start (old way, out of date)
===
 DISCLAIMER: I don't use this way anymore.

### Preliminaries:  get a dataset and set up a project.

```
#
# set up a project
#
# --> create a directory for your project
mkdir -p ./myproject/data
# --> copy the examples directory (from this repo)
cp -rf ./examples ./myproject/
# --> link your pre-trained torch models into ./data if you want.
ln -sr ~/.torch ./myproject/data/torch
# --> now go download the RITE dataset and unzip it into ./myproject/data/RITE
ls ./myproject/data/RITE
# ls output: AV_groundTruth.zip  introduction.txt  read_me.txt  test  training

cd ./myproject
# --> ask Python to register the code in ./examples as a package
export PYTHONPATH=.:$PYTHONPATH
```

### Train the model from command-line and get results

```
#
# train the model from command-line
#
simplepytorch ./examples/ -h
simplepytorch ./examples/ LetsTrainSomething -h
simplepytorch ./examples/ LetsTrainSomething --run-id experimentA --epochs 3
# alternative command-line ways to start code
run_id=experimentB epochs=3 simplepytorch ./examples/ LetsTrainSomething
simplepytorch ./examples/my_feedforward_model_config.py LetsTrainSomething

# --> debug your model with IPython
simplepytorch_debug ./examples/ LetsTrainSomething --run-id experimentA --epochs a
# --> now you can type %debug to drop into a PDB debugger.  Move around by typing `up` and `down`

# check the results
ls ./data/results/experimentA
tail -f ./data/results/experimentA/perf.csv 
# --> plot results for all experiments matching a regex
simplepytorch_plot 'experiment.*' --ns
```

### Programmatic access via the simplepytorch API:

```
import examples
import simplepytorch.api as api

cfg = api.load_model_config(examples.LetsTrainSomething, '--epochs 1')
cfg.train()
```

### Developing your own pytorch code

Check the examples directory for a simple getting started template.  You
can train a model to perform vessel segmentation on the RITE dataset in
about 70 lines of code.

[examples/](examples/)

<!-- TODO -->
<!-- You can also look at prior work using this library.  If you would
like to add your (preferably published and) reproducible work to this list,
please make a PR and update the README! -->

<!-- - [Pixel Color Amplification (ICIAR 2020)]() -->
<!-- - [O-MedAL (Wiley DMKD 2020)](https://github.com/adgaudio/o-medal) Early version of this library developed mostly here, so perhaps not a great example. -->

As a next step, you can copy the examples directory, rename it to
whatever your project name is and start from there.  You will find, as
mentioned in `examples/my_feedforward_model_config.py` that
the api.FeedForward class typically lists everything needed.  Assuming
you want to use the FeedForward class, just implement or override its
methods.  If something isn't obvious or clear, create a GitHub issue.  I
will support you to the extent that I can.


**Datasets:**

The library provides PyTorch Dataset implementations for datasets 
without an already existing PyTorch implementation.

To use the pre-defined dataset classes, you must download the data and
unzip it yourself.  Consult Dataset class docstring for usage details.

```
import simplepytorch.datasets as D

dset = D.RITE(use_train_set=True)
dset[0]
```

For example, some downloaded datasets I use have the following structure:

```
 $ ls data/{arsn_qualdr,eyepacs,messidor,IDRiD_segmentation,RITE}
data/IDRiD_segmentation:
'1. Original Images'  '2. All Segmentation Groundtruths'   CC-BY-4.0.txt   LICENSE.txt

data/RITE:
AV_groundTruth.zip  introduction.txt  read_me.txt  test  training

data/arsn_qualdr:
README.md  annotations  annotations.zip  imgs1  imgs1.zip  imgs2  imgs2.zip

data/eyepacs:
README.md                 test          test.zip.003  test.zip.006  train.zip.001  train.zip.004
sample.zip                test.zip.001  test.zip.004  test.zip.007  train.zip.002  train.zip.005
sampleSubmission.csv.zip  test.zip.002  test.zip.005  train         train.zip.003  trainLabels.csv.zip

data/messidor:
Annotation_Base11.csv  Annotation_Base21.csv  Annotation_Base31.csv  Base11  Base21  Base31
Annotation_Base12.csv  Annotation_Base22.csv  Annotation_Base32.csv  Base12  Base22  Base32
Annotation_Base13.csv  Annotation_Base23.csv  Annotation_Base33.csv  Base13  Base23  Base33
Annotation_Base14.csv  Annotation_Base24.csv  Annotation_Base34.csv  Base14  Base24  Base34
```
