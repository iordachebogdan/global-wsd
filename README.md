## Ant Colony + Firefly WSD

In order to run this project, firstly ensure that you have `python 3.10` installed along with the dependencies listed in `requirements.txt`.

The experiment configuration must be specified in the `config.json` file. A `predictions` directory must be present in order to store the algorithm's predictions for a dataset. To run an experiment:

``` bash
mkdir -p predictions
python3.10 run.py
python3.10 compute_metrics.py /path/to/generated/prediction/json
```

### Experiment Configuration

Description of the `config.json` file:
 * `dataset_name`: the name of the dataset to run the experiment on (it can be `semeval`, `senseval2`, `senseval3`, `semcor`)
 * `dataset_config`: should be an empty object for `semcor` or an object providing the path to the XML file containing the documents (`docs_path`) and the path to the gold labels (`gs_path`), for the other datasets
 * `algorithm_name`: can be `antcolony` or `firefly`
 * `algorithm_config`: an object containing the algorithm hyperparameters
     * for `antcolony`:
         * `energy_ant`: how much energy one ant can gather at one step
         * `max_energy`: maximum carry capacity of an ant
         * `evaporation_rate`: percentage for evaporation rate of pheromone trails
         * `energy_node`: initial energy in all nodes
         * `ant_cycles`: lifespan of an ant
         * `max_odour`: maximum length for odour vector
         * `odour_deposit_pct`: percentage of odour vector components deposited by an ant
         * `total_cycles`: number of iterations in the algorithm
         * `theta`: how much pheromone is left by an ant when traversing an edge
     * for `firefly`:
         * `swarm_size`: number of fireflies
         * `window_size`: for computing the fireflies' light intensities
         * `max_synsets`: maximum number of senses to consider for a word (the first senses)
         * `num_iterations`: number of HFA cycles
         * `gamma`: light absorption coefficient
         * `alpha`: percantage for randomized movement of firefiles
         * `lr`: probability of starting LAHC search at the end of a cycle
         * `lfa`: length of fitness list in LAHC
         * `lahc_cycles`: number of iterations in LAHC
         * `lahc_num_switches`: for NS given a firefly, change randomly the senses of this many words
 * `lesk_config`:
     * `vocab_path`: where to store/load the vocabulary used for processing glosses
     * `use_squares`: controls if we want to compute overlaps using a squared weight for longer common phrases
     * `relations_list`: corresponds to the first behaviour of the algorithm, when computing the score for two synsets calculate the overlap between the entire extended gloss of the first one with that of the second one. Extended glosses are computed all the specified relations
     * `relation_pairs`: corresponds to the second behaviour; it is a list of pairs of synset relations; if defined the scores will be computed by summing the overlaps calculated between the gloss obtained from the relation on the first position in the pair for the first synset, and the gloss obtained from the second relation for the second synset.
